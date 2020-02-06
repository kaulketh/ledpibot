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

from config import token, access, commands, wrong_id, pls_select, not_allowed, called
import logger
from control import run_thread, stop_threads

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger('LedPiBot')
assert isinstance(token, str)
bot = telepot.Bot(token)
answerer = telepot.helper.Answerer(bot)
admins = [access.thk, access.annib]

# region Keyboards
stop = commands[0]
start = commands[1]


def _btn(text):
    return KeyboardButton(text=text.title())


kb_markup = ReplyKeyboardMarkup(keyboard=[
    [_btn(commands[2]), _btn(commands[3]), _btn(commands[6]), _btn(commands[7]), _btn(commands[16])],
    [_btn(commands[15])],
    [_btn(commands[8]), _btn(commands[9]), _btn(commands[10]),
     _btn(commands[11]), _btn(commands[12]), _btn(commands[13]), _btn(commands[14])],
    [_btn(commands[4]), _btn(commands[5]), _btn(commands[17])]
])

rm_kb = ReplyKeyboardRemove()


def _kb_stop(func):
    return ReplyKeyboardMarkup(keyboard=[
        [_btn(stop.title() + ' \"' + func.title() + '\"')]
    ])


# endregion
# region Methods


def _send(chat_id, text, reply_markup=kb_markup, parse_mode='Markdown'):
    bot.sendMessage(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)


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


# noinspection PyGlobalUndefined
def _on_chat_message(msg):
    global command
    content_type, chat_type, chat_id = telepot.glance(msg)
    log.debug(msg)

    if chat_id not in admins:
        _reply_wrong_id(chat_id, msg)
        return

    if content_type == 'text':
        command = msg['text']
        log.info('Command = ' + command)
        # start
        if (command.title() == start.title()) or (command == ('/' + start)):
            _send(chat_id, pls_select.format(msg['from']['first_name']))
        # stop if command starts with 'stop' or '/stop'
        elif (command.title().startswith(stop.title())) or (command.startswith('/' + stop)):
            stop_threads()
            _send(chat_id, pls_select.format(msg['from']['first_name']))
        # all others
        elif any(c for c in commands if (command.title()) == (c.title())):
            _send(chat_id, '*' + command.title() + called, reply_markup=_kb_stop(command))
            run_thread(command)
        else:
            _reply_wrong_command(chat_id, command)
    else:
        _reply_wrong_command(chat_id, content_type)


# endregion


MessageLoop(bot, {'chat': _on_chat_message}).run_as_thread()
log.debug('Bot is listening ...')
while True:
    try:
        time.sleep(5)

    except KeyboardInterrupt:
        log.warning('Program interrupted')
        exit()

    except Exception as e:
        log.error('An error occurs: ' + str(e))
