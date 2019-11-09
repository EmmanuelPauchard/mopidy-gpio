#!/usr/bin/python
# -*- coding: utf-8 -*-

import pykka

from mopidy import core
from threading import Timer

import logging
from RPi import GPIO

logger = logging.getLogger(__name__)

button_pud = "PUD_UP"
button_logical_level = "LOW"
button_config = {15: ("m3u:2", 14),
                 24: ("m3u:3", 23),
                 8: ("m3u:1", 25),
                 20: ("m3u:4", 16),
                 3: ("m3u:5", 4)}

button_event_direction = {"LOW": GPIO.FALLING,
                          "HIGH": GPIO.RISING}

class GpioFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(GpioFrontend, self).__init__()
        logger.info("Starting Mopidy GPIO frontend")

        self.core = core
	self.current_uri = "" 

        # fixme: can't get our config validated by mopidy - nevermind
        self.logical_active_level = getattr(GPIO, button_logical_level)
        self.button_config = button_config
        self.filter_ms = 100

        # set up GPIOs
        GPIO.setmode(GPIO.BCM)
        for button_gpio, (action, led_gpio) in self.button_config.items():
            GPIO.setup(button_gpio, GPIO.IN, pull_up_down=getattr(GPIO, button_pud))
            if led_gpio:
                GPIO.setup(led_gpio, GPIO.OUT, initial=GPIO.LOW)
            GPIO.add_event_detect(button_gpio, button_event_direction[button_logical_level], self._filter, 300)

    def _is_gpio_active(self, value):
        """
        Compare input value to the configured logical "active" level
        Returns True if value correponds to active level, False otherwise
        """
        return value == self.logical_active_level

    def _filter(self, channel):
        """
        Filter out spurious transitions of less than self.filter_ms - by the way, discard RISING transitions
        """
        if self._is_gpio_active(GPIO.input(channel)):
            Timer(self.filter_ms / 1000, self._check_filter, [channel]).start()

    def _check_filter(self, channel):
        """
        Confirm filtered entry if level is still active
        """
        if self._is_gpio_active(GPIO.input(channel)):
            self.trigger(channel)

    def trigger(self, channel):
        """
        Launch action configured for that button
        Switch corresponding LED on, switch all other LEDs off
        :param: channel: the GPIO channel (BCM mode)
        """
        action, led = self.button_config[channel]
	if self.current_uri == action:
            logger.info("GPIO frontend: Next (multiple press)")
 	    self.core.playback.next()
            return
	else:
            self.current_uri = action		

        if "m3u:" == action[:4]:
            self.set_playlist(action[4:])
        elif "toggle" == action:
            self.play_pause()
        elif "next" == action:
            logger.info("GPIO frontend: Next")
            self.core.playback.next()
        elif "previous" == action:
            logger.info("GPIO frontend: Previous")
            self.core.playback.previous()

        if led:
            for _, a_led in self.button_config.values():
                GPIO.output(a_led, GPIO.LOW)
            GPIO.output(led, GPIO.HIGH)

    def set_playlist(self, name):
        logger.info("GPIO frontend: Set playlist to {}".format(name))
        self.core.tracklist.clear()
        for playlist in self.core.playlists.playlists.get():
            if playlist.name == name:
                for track in playlist.tracks:
                    self.core.tracklist.add(uri=track.uri)
        self.core.playback.play()

    def play_pause(self):
        if self.core.playback.state.get() == core.PlaybackState.PLAYING:
            logger.info("GPIO frontend: Pause")
            self.core.playback.pause()
        elif self.core.playback.state.get() == core.PlaybackState.STOPPED:
            logger.info("GPIO frontend: Play")
            self.core.playback.play()
        elif self.core.playback.state.get() == core.PlaybackState.PAUSED:
            logger.info("GPIO frontend: Resume")
            self.core.playback.resume()
