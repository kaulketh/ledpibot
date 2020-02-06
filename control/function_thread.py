#!/usr/bin/python3
# -*- coding: utf-8 -*-

import threading

import logger
from control.led_strip import LED_BRIGHTNESS
from functions import clear

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger("LightFunctionsThread")


class LightFunctionsThread(threading.Thread):
    def __init__(self, function, name, strip):
        super(LightFunctionsThread, self).__init__()
        self._paused = True
        self._state = threading.Condition()
        self._function = function
        self._name = name
        self._strip = strip
        self._stop = threading.Event()
        log.debug('Thread \'{0}\' initialized for \'{1}\' as \'{2}\''.format(name, function, self._name))

    def start(self):
        super(LightFunctionsThread, self).start()
        log.debug('Start thread \'{0}\''.format(self._name))

    def run(self):
        self.resume()  # unpause self for first run
        log.debug('Run thread \'{0}\''.format(self._name))
        while True:
            with self._state:
                if self._paused:
                    clear(self._strip)
                    self._state.wait()  # block until notified
            while not self._paused:
                try:
                    # Call function
                    self._function(self._strip)
                except Exception as e:
                    log.error('An error occurs: ' + str(e))
                    exit()

    def resume(self):
        with self._state:
            self._paused = False
            self._state.notify()
        log.debug('Thread \'{0}\' resume: {1}'.format(self._name, str(not self._paused)))

    def pause(self):
        with self._state:
            self._paused = True
            clear(self._strip)
        log.debug('Thread \'{0}\' pause: {1}'.format(self._name, str(self._paused)))

    def stop(self):
        self._stop.set()
        self._strip.setBrightness(LED_BRIGHTNESS)
        clear(self._strip)
        log.debug('Thread \'{0}\' stop: {1}'.format(self._name, str(self.stopped())))

    def stopped(self):
        return self._stop.is_set()
