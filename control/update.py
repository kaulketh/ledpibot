#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import os

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
        self.remove_clone = 'rm -rf ledpibot/'
        self.clone = 'git clone -v https://github.com/kaulketh/ledpibot.git -b ' + self.branch
        self.log = logger.get_logger(self.name)
        self.folder = os.path.dirname(os.path.abspath(__file__))
        self.root_folder = os.path.join(self.folder, '..')
        self.subs = [f for f in os.listdir(self.root_folder)]

    def run(self):
        self.log.info('Starting update...')
        try:
            self.log.info('Clone branch \'' + self.branch + '\' from Github repository...')
            os.system(self.clone)
            cloned_f = [f for f in os.listdir('ledpibot') if not f.startswith('.')]
            self.log.info('Copy files and folders...')
            for f in cloned_f:
                os.system('cp -rv ledpibot/' + f + ' /home/pi/bot/')
            self.log.info('Remove not needed files...')
            os.system(self.remove_clone)
        except Exception as e:
            self.log.error('Update failure: ' + str(e))
            return False
        return True


if __name__ == '__main__':
    pass
