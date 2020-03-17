#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import os
import subprocess

from control.autoreboot import AutoReboot
from logger import LOGGER as LOG
from .update import Update

NAME = "Service"
reboot = "shutdown -r now"

new_line = "\n"
empty = ""
menu_header = f"{NAME} functions:"
c_prefix = "- "
c_system = "/serviceUsage"
c_reboot = "/serviceReboot"
c_update = "/serviceUpdate"

menu_dictionary = {
    0: c_reboot,
    1: c_system,
    2: c_update
}


# noinspection PyShadowingNames
def build_menu():
    menu = f"{menu_header}{new_line}"
    LOG.debug(f"Build service menu: {menu.replace(new_line, empty)}")
    for key in menu_dictionary.keys():
        line = f"{c_prefix}{menu_dictionary.get(key)}{new_line}"
        menu += line
        LOG.debug(f"Add line to menu: {line.replace(new_line, empty)}")
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
    return f"{host}{new_line}{ip}{new_line}{m}{new_line}{d}{new_line}{c}" \
        .replace("b'", "").replace("'", "").replace("\\n", "")


def reboot_device(log_msg: str = None):
    try:
        LOG.info(log_msg)
        os.system(reboot)
    except Exception as e:
        LOG.error(f"{e}")


def update_bot(log_msg: str):
    try:
        LOG.info(log_msg)
        if Update().run():
            reboot_device('Update done.')
        else:
            LOG.warning('Update failed.')
    except Exception as e:
        LOG.error(f"{e}")


def init_auto_reboot(time):
    try:
        AutoReboot(time).start()
        return
    except Exception as e:
        LOG.error(f"{e}")


try:
    menu = build_menu()
except Exception as ex:
    LOG.error(f"{ex}")

if __name__ == '__main__':
    pass
