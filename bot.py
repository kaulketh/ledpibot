#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import codecs
import time

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import logger
from config import \
    token, access, commands, wrong_id, pls_select, not_allowed, called, started, cleared, rebooted, rotated, stopped
from control import run_thread, stop_threads, service

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger('LedPiBot')
assert isinstance(token, str)
bot = telepot.Bot(token)
answerer = telepot.helper.Answerer(bot)
admins = [access.thk, access.annib]
messages = []

# region Keyboards
stop = commands[0]
start = commands[1]


def _btn(text):
    return KeyboardButton(text=text)


kb_markup = ReplyKeyboardMarkup(keyboard=[
    [_btn(commands[2]), _btn(commands[3]), _btn(commands[6]), _btn(commands[7]), _btn(commands[16])],
    [_btn(commands[4]), _btn(commands[5]), _btn(commands[17])],
    [_btn(commands[15])],
    [_btn(commands[8]), _btn(commands[9]), _btn(commands[10]),
     _btn(commands[11]), _btn(commands[12]), _btn(commands[13]), _btn(commands[14])]
])

rm_kb = ReplyKeyboardRemove()


def _kb_stop(func):
    return ReplyKeyboardMarkup(keyboard=[[_btn(stop + ' \"' + func + '\"')]])


# endregion
# region Methods
def _welcome():
    log.debug('Bot is listening ...')
    # for admin in admins:
    #     _send(admin, started)
    _send(admins[0], started)


def _send(chat_id, text, reply_markup=kb_markup, parse_mode='Markdown'):
    log.debug("Message posted: {0}|{1}|{2}|{3}".format(str(chat_id), text, str(reply_markup), str(parse_mode)))
    mid = (bot.sendMessage(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode))['message_id']
    _store_msg_id(mid)


def _reply_wrong_id(chat_id, msg):
    user_id = msg['from']['id']
    first_name = msg['from']['first_name']
    last_name = msg['from']['last_name']
    username = msg['from']['username']
    _send(chat_id, wrong_id.format(user_id, username, first_name, last_name), reply_markup=rm_kb)
    log.warning('Unauthorized access: ID {0} User:{1}, {2} {3} '.format(chat_id, username, first_name, last_name))


# noinspection PyGlobalUndefined
def _reply_wrong_command(chat_id, content):
    global got
    try:
        got = str(codecs.encode(content, 'utf-8')).replace('b', '').title()
        raise Exception('Not allowed input: ' + got)
    except Exception as ex:
        _send(chat_id, not_allowed, parse_mode='MarkdownV2')
        log.warning(str(ex))
    return


def _clear_history(chat_id, add_msg='', reply_markup=rm_kb):
    global messages
    messages = service.clear_history(bot, chat_id, messages, cleared)
    _send(chat_id, cleared + ' ' + add_msg, reply_markup=reply_markup)


def _store_msg_id(msg_id: int):
    global messages
    messages.append(msg_id)
    log.debug('Message ID stored: ' + str(msg_id))


# noinspection PyGlobalUndefined
def _on_chat_message(msg):
    global command
    content_type, chat_type, chat_id = telepot.glance(msg)

    log.debug(msg)
    _store_msg_id(msg['message_id'])

    # check user
    if chat_id not in admins:
        _reply_wrong_id(chat_id, msg)
        return

    if content_type == 'text':
        command = msg['text']
        log.info('Requested: ' + command)
        # start or /start
        if (command == start) or (command == start.lower()) or (command == ('/' + start.lower())):
            _send(chat_id, pls_select.format(msg['from']['first_name']))
        # stop(function)
        elif (command.startswith(stop)) or (command.startswith(stop.lower())):
            if stop_threads():
                _send(chat_id, pls_select.format(msg['from']['first_name']))
        # /stop
        elif command.startswith('/' + stop.lower()):
            if stop_threads():
                _clear_history(chat_id, stopped)
        # service or /service
        elif (command.startswith(service.name)) \
                or (command.startswith(service.name.lower())) or (command.startswith('/' + service.name.lower())):
            if stop_threads():
                _send(chat_id, service.menu, reply_markup=rm_kb)
                if command == service.c_rotate:
                    service.log_rotate_bot(rotated)
                    _send(chat_id, rotated, reply_markup=rm_kb)
                elif command == service.c_reboot:
                    _clear_history(chat_id, rebooted)
                    service.reboot_device(rebooted)
                elif command == service.c_clear:
                    _clear_history(chat_id, '\n' + pls_select.format(msg['from']['first_name']), kb_markup)
        # all other commands
        elif any(c for c in commands if (command == c)):
            _send(chat_id, called.format(command), reply_markup=_kb_stop(command))
            run_thread(command)
        else:
            _reply_wrong_command(chat_id, command)
    else:
        _reply_wrong_command(chat_id, content_type)


# endregion


MessageLoop(bot, {'chat': _on_chat_message}).run_as_thread()
_welcome()
while True:
    try:
        time.sleep(5)

    except KeyboardInterrupt:
        log.warning('Program interrupted')
        exit()

    except Exception as e:
        log.error('An error occurs: ' + str(e))
