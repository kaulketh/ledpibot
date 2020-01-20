#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

from logger import logger

log = logger.get_logger("RaspberryThread")


class RaspberryThread(threading.Thread):
    def __init__(self, function, name):
        self.paused = True
        self.state = threading.Condition()
        self.function = function
        super(RaspberryThread, self).__init__()
        self._stop = threading.Event()
        log.debug('{0} initialized for {1} as {2}'.format(name, self.function, self.name))
        self.name = name

    def start(self):
        super(RaspberryThread, self).start()
        log.debug('{0} start'.format(self.name))

    def run(self):
        # self.resume() #unpause self
        log.debug('{0} run'.format(self.name))
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # block until notifed
            while not self.paused:
                # Call function
                self.function()

    def resume(self):
        log.debug('{0} resume'.format(self.name))
        with self.state:
            self.paused = False
            self.state.notify()

    def pause(self):
        log.debug('{0} pause'.format(self.name))
        with self.state:
            self.paused = True

    def stop(self):
        log.debug('{0} stopped'.format(self.name))
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
