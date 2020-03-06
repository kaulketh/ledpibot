#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

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
        self.prepare = 'touch tmp'
        self.remove_clone = 'rm -rfv ledpibot/'
        self.clone = 'git clone -b ' + self.branch + ' https://github.com/kaulketh/ledpibot'
        self.log = logger.get_logger(self.name)
        self.folder = os.path.dirname(os.path.abspath(__file__))
        self.subfolders = [f.path for f in os.scandir(self.folder) if f.is_dir()]

    # Execute bash command, assign default output (stdout 1 and stderr 2) to file, read in variable and get back
    # noinspection PyMethodMayBeStatic
    def _os_cmd(self, cmd: str) -> str:
        os.system(cmd + ' > tmp 2>&1')
        file = open('tmp', 'r')
        data = file.read()
        file.close()
        return data.replace('\n', '')

    def run(self):
        self.log.info('Starting update...')
        try:
            self.log.info(self._os_cmd(self.save_secret))
            self.log.info('Delete old folders.')
            for f in self.subfolders:
                if not f == "logs":
                    os.system('rm -rf ' + f)
            os.system(self.prepare)
            self.log.info('Clone from repository')
            os.system(self.clone)

            cloned_f = [f for f in os.listdir('ledpibot')]
            self.log.info('Copy files and folders...')
            for f in cloned_f:
                if not f.startswith('.'):
                    os.system('mv -fv ledpibot/' + f + ' ' + f)
            self.log.info('Remove not needed files...')
            os.system(self.remove_clone)
            self.log.info(self._os_cmd(self.restore_secret))
        except Exception as e:
            self.log.error('Update failure: ' + str(e))
            return False
        return True


if __name__ == '__main__':
    pass
