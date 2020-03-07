#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import os
import sys

import logger


class Update:
    def __init__(self, branch: str = None):
        self.name = "update"
        if branch is None:
            self.branch = 'master'
        else:
            self.branch = branch
        self.save_secret = 'mv -v config/secret.py secret.py'
        self.restore_secret = 'mv -v secret.py config/secret.py'
        self.prepare = 'touch tmp'
        self.remove_clone = 'rm -rf ledpibot/'
        self.clone = 'git clone -b ' + self.branch + ' https://github.com/kaulketh/ledpibot'
        self.log = logger.get_logger(self.name)
        self.folder = os.path.dirname(os.path.abspath(__file__))
        self.root_folder = os.path.join(self.folder, '..')
        self.subs = [f for f in os.listdir(self.root_folder)]

    # Execute bash command, assign default output (stdout 1 and stderr 2) to file, read in variable and get back
    # noinspection PyMethodMayBeStatic
    def _os_cmd(self, cmd: str) -> str:
        os.system(cmd + ' > tmp 2>&1')
        file = open('tmp', 'r')
        data = file.read()
        file.close()
        return data.replace('\n', ' ')

    def run(self):
        self.log.info('Starting update...')
        try:
            os.system(self.prepare)
            self.log.info('Clone from repository...')
            os.system(self.clone)
            cloned_f = [f for f in os.listdir('ledpibot') if not f.startswith('.')]
            self.log.info('Copy files and folders...')
            for f in cloned_f:
                self.log.debug(self._os_cmd('cp -rv ledpibot/' + f + ' /home/pi/bot/'))
            self.log.info('Remove not needed files...')
            self.log.debug(self._os_cmd(self.remove_clone))
        except Exception as e:
            self.log.error('Update failure: ' + str(e))
            return False
        return True


if __name__ == '__main__':
    pass
