#!/usr/bin/python3
# -*- coding: utf-8 -*-
# control/service.py
"""
Service functions
"""

import os

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

name = "service"
log = logger.get_logger(name.title())

markdown = "-d parse_mode='Markdown'"
c_rotate = "/servicerotate"
c_reboot = "/servicereboot"
c_clear = "/serviceclear"
menu = "Service functions:\n- {0}\n- {1}\n- {2}".format(c_rotate, c_reboot, c_clear)

log_rotate = 'logrotate -f /etc/logrotate.conf &'
reboot = 'shutdown -r now'


def reboot_device(log_msg):
    try:
        log.info(log_msg)
        os.system(reboot)
    except Exception as e:
        log.error(str(e))


def log_rotate_bot(log_msg):
    try:
        log.info(log_msg)
        os.system(log_rotate)
    except Exception as e:
        log.error(str(e))


def clear_history(bot, chat_id, messages, log_msg):
    for msg in messages:
        try:
            bot.deleteMessage((chat_id, msg,))
        except Exception as e:
            log.error(str(e))
    messages.clear()
    log.info(log_msg)
    return messages
