#!/usr/bin/python3
# -*- coding: utf-8 -*-
# control/service.py
"""
Service functions
"""
__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import datetime
import os
import signal
import subprocess
import time

import logger
from control import CountdownThread

NAME = "Service"
LOG = logger.get_logger(NAME)

log_rotate = 'logrotate -f /etc/logrotate.conf &'
reboot = 'shutdown -r now'
get_pid = "ps -o pid,args -C python3 | awk \'/bot.py/ { print $1 }\'"

line_break = "\n"
menu_header = NAME + " functions:"
c_prefix = "- "
c_test = "/serviceTest"
c_system = "/serviceUsage"
c_rotate = "/serviceRotate"
c_reboot = "/serviceReboot"
c_kill = "/serviceKill"
c_update = "/serviceUpdate"

menu_dictionary = {
    # 0: c_kill,
    1: c_reboot,
    2: c_system,
    # 3: c_rotate,
    4: c_update,
    # 5: c_test
}


# noinspection PyShadowingNames
def build_menu():
    menu = "{0}{1}".format(menu_header, line_break)
    LOG.debug('Build service menu: ' + menu.replace(line_break, ""))
    for key in menu_dictionary.keys():
        line = "{0}{1}{2}".format(c_prefix, menu_dictionary.get(key), line_break)
        menu += line
        LOG.debug('Add line to menu: ' + line.replace(line_break, ""))
    return menu


def system_usage():
    host = subprocess.check_output("hostname", shell=True).upper()
    ip = "IP :  " + str(subprocess.check_output("hostname -I | cut -d\' \' -f1", shell=True))
    m = subprocess.check_output(
        "free -m | awk 'NR==2{printf \"Memory :  %s / %s MB (%.0f%%)\", $3,$2,$3*100/$2 }'", shell=True)
    d = subprocess.check_output(
        "df -h | awk '$NF==\"/\"{printf \"Disk :  %d / %d GB (%s)\", $3,$2,$5}'", shell=True)
    c = subprocess.check_output(
        "top - bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\\([0-9.]*\\)%* id.*/\\1/\" | "
        "awk '{print \"CPU Load :  \"100 - $1\"%\"}'", shell=True)
    return "{5}{0}{4}{0}{1}{0}{2}{0}{3}".format(line_break, m, d, c, ip, host) \
        .replace("b'", "").replace("'", "").replace("\\n", "")


def reboot_device(log_msg: str = None):
    try:
        LOG.info(log_msg)
        os.system(reboot)
    except Exception as e:
        LOG.error(str(e))


def log_rotate_bot(log_msg: str):
    try:
        LOG.info(log_msg)
        os.system(log_rotate)
    except Exception as e:
        LOG.error(str(e))


def kill_bot(log_msg: str = None, sig=signal.SIGTERM):
    pid = os.getpid()
    if log_msg is not None:
        LOG.info(log_msg)
    try:
        result = 0
        LOG.debug('Command "kill {0}" returned {1}\n'.format(pid, os.kill(pid, sig)))
    except Exception as e:
        LOG.error('Command "kill {0}" raised exception {1}\n'.format(pid, e))
        result = e
    return result == 0


def update_bot(log_msg: str):
    LOG.info(log_msg)
    from .update import Update
    if Update('develop').run():
        reboot_device('Update done.\n')
        return True
    else:
        LOG.error('Update failed.')
        return False


def init_auto_reboot():
    name = "Auto reboot"

    def is_midnight():
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        sec = datetime.datetime.now().second
        about_midnight = ((hour == minute == 0) and (0 <= sec <= 5))
        # for test only
        # anytime = (hour == 21 and minute == 30 and sec == 0)
        # return anytime
        return about_midnight

    class AutoReboot(CountdownThread):
        def __init__(self):
            super(AutoReboot, self).__init__(None, None, name=name, n=0)

        def _process(self):
            pass

        def run(self):
            LOG.info("Auto reboot initialized for midnight")
            while not is_midnight():
                time.sleep(2)
            from bot import external_request
            external_request(name)
            reboot_device(name)

    AutoReboot().start()
    return


menu = build_menu()

if __name__ == '__main__':
    pass
