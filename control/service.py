#!/usr/bin/python3
# -*- coding: utf-8 -*-
# control/service.py
"""
Service functions
"""

import os
import subprocess

from telepot import Bot

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

name = "Service"
log = logger.get_logger(name.title())

markdown = "-d parse_mode='Markdown'"
c_system = "/serviceUsage"
c_rotate = "/serviceRotate"
c_reboot = "/serviceReboot"
c_clear = "/serviceClear"
menu = "Service functions:\n- {0}\n- {1}\n- {2}\n- {3}".format(c_rotate, c_reboot, c_clear, c_system)

log_rotate = 'logrotate -f /etc/logrotate.conf &'
reboot = 'shutdown -r now'


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
    br = "\n"
    return "{5}{0}{4}{0}{1}{0}{2}{0}{3}".format(br, m, d, c, ip, host) \
        .replace("b'", "").replace("'", "").replace("\\n", "")


def reboot_device(log_msg: str):
    try:
        log.info(log_msg)
        os.system(reboot)
    except Exception as e:
        log.error(str(e))


def log_rotate_bot(log_msg: str):
    try:
        log.info(log_msg)
        os.system(log_rotate)
    except Exception as e:
        log.error(str(e))


def clear_history(bot: Bot, chat_id: int, messages: list, log_msg: str):
    """
    :param bot: Bot
    :param chat_id: Chat ID
    :param messages: List of stored message IDs
    :param log_msg: Message to use in logger
    :return: Empty list
    """
    for msg in messages:
        try:
            bot.deleteMessage((chat_id, msg,))
            log.debug('Delete message: ID {0}'.format(str(msg)))
        except Exception as e:
            log.warning('Error while deleting message: ID {0}'.format(str(msg)))
            log.error("{0:.<55}".format(str(e)[0:50]))
    messages.clear()
    log.info(log_msg)
    return messages
