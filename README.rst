****************************
Mopidy-gpio
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-gpio.svg?style=flat
    :target: https://pypi.org/project/Mopidy-gpio/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/EmmanuelPauchard/mopidy-gpio/master.svg?style=flat
    :target: https://travis-ci.org/EmmanuelPauchard/mopidy-gpio
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/EmmanuelPauchard/mopidy-gpio/master.svg?style=flat
   :target: https://coveralls.io/r/EmmanuelPauchard/mopidy-gpio
   :alt: Test coverage

GPIO controlled Mopidy frontend


Installation
============

Install by running::

    pip install Mopidy-gpio

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<https://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-gpio to your Mopidy configuration file::

    [gpio]

    .. confval:: gpio/button_pud

        Configure button pull up/down here - must comply to RPi.GPIO syntax, ie: PUD_UP, PUD_DOWN


    .. confval:: gpio/button_logical_level

        Configure button logical active level - must comply to RPi.GPIO syntax, ie: LOW, HIGH


    .. confval:: gpio/button_config

        gpio config is a map of {PIN number (int, BCM mode): (uri to play (string) or ("stop"|"toggle"), LED name (int, BCM mode))}
        If LED name is not None, then the LED will be powered on when uri is started, while all other LED will be switched off


.. note::
    Using this package requires to be part of the "gpio" group.
    If running Mopidy as a service, make sure you have added user "mopidy" to the "gpio" group.

Project resources
=================

- `Source code <https://github.com/EmmanuelPauchard/mopidy-gpio>`_
- `Issue tracker <https://github.com/EmmanuelPauchard/mopidy-gpio/issues>`_
- `Changelog <https://github.com/EmmanuelPauchard/mopidy-gpio/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Emmanuel Pauchard <https://github.com/EmmanuelPauchard>`__
- Current maintainer: `Emmanuel Pauchard <https://github.com/EmmanuelPauchard>`__
- `Contributors <https://github.com/EmmanuelPauchard/mopidy-gpio/graphs/contributors>`_


Usage
=======

- Project goals
Create a very simple HMI to a Raspberry PI used as a music player. The controls are push-buttons where each button is associated with a playlist. When button is pressed, the playlist should start.

- Design planning

# Configure plugin to find and initialize playlists
# Create configuration file syntax and example (needs: associate button/playlist)
# Add remote playlist (web radio, podcast)
# Add volume control by external potentiometer
