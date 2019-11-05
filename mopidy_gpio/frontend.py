#!/usr/bin/python
# -*- coding: utf-8 -*-

import pykka

from mopidy import core

import logging
from RPi import GPIO

logger = logging.getLogger(__name__)

class GpioFrontend(pykka.ThreadingActor, core.CoreListener):
    def __init__(self, config, core):
        super(GpioFrontend, self).__init__()
        self.core = core

        logger.info("Starting Mopidy GPIO frontend")

        # set up GPIOs
        GPIO.setmode(GPIO.BCM)
        #Fixme: add config
        GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(14, GPIO.FALLING, self.play_pause, 1000)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(15, GPIO.FALLING, self.set_playlist, 1000)

        self.playlists = ["vivaldi", "bach", "bizet", "tchaikowsky"]
        self.current_playlist = 0

    def set_playlist(self, channel):
        self.current_playlist = (self.current_playlist + 1) % len(self.playlists)
        logger.info("Set playlist to {}".format(self.playlists[self.current_playlist]))
        self.core.tracklist.clear()
        for playlist in self.core.playlists.playlists.get():
            logger.info("\t playlist: {}".format(playlist))
            if playlist.name == self.playlists[self.current_playlist]:
                for track in playlist.tracks:
                    self.core.tracklist.add(uri=track.uri)
        self.core.playback.play()

    def play_pause(self, channel):
        logger.info("GPIO frontend: Toggle")
        if self.core.playback.state.get() == core.PlaybackState.PLAYING:
            logger.info("GPIO frontend: Pause")
            self.core.playback.pause()
        elif self.core.playback.state.get() == core.PlaybackState.STOPPED:
            logger.info("GPIO frontend: Play")
            self.core.playback.play()
        elif self.core.playback.state.get() == core.PlaybackState.PAUSED:
            logger.info("GPIO frontend: Resume")
            self.core.playback.resume()

    def next(self, channel):
        logger.info("GPIO frontend: next")
        self.core.playback.next()