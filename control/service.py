#!/usr/bin/python3
# -*- coding: utf-8 -*-
# control/service.py
"""
Service functions
"""

import os

from telepot import Bot

import logger

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

name = "service"
log = logger.get_logger(name.title())

markdown = "-d parse_mode='Markdown'"
c_rotate = "/serviceRotate"
c_reboot = "/serviceReboot"
c_clear = "/serviceClear"
menu = "Service functions:\n- {0}\n- {1}\n- {2}".format(c_rotate, c_reboot, c_clear)

log_rotate = 'logrotate -f /etc/logrotate.conf &'
reboot = 'shutdown -r now'


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
            log.warning('Minor error while deleting message: ID {0}'.format(str(msg)))
    messages.clear()
    log.info(log_msg)
    return messages
