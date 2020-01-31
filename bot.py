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

# to set language select import accordingly
from config import lang_de as language  # German language
# from config import lang_en as language  # English language
import config
import logger
from config.commands import commands
from control import run_thread, stop_threads

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

log = logger.get_logger('LedPiBot')

assert isinstance(config.token, str)
bot = telepot.Bot(config.token)
answerer = telepot.helper.Answerer(bot)
admins = [config.access.thk, config.access.annib]
functions_kb_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=commands[1].title()), KeyboardButton(text=commands[2].title()),
     KeyboardButton(text=commands[3].title())],
    [KeyboardButton(text=commands[4].title()), KeyboardButton(text=commands[5].title()),
     KeyboardButton(text=commands[6].title())]
])
remove_kb = ReplyKeyboardRemove()


def _stop_kb(func):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=commands[7].title() + ' \"' + func.title() + '\"')]
    ])


def _reply_wrong_id(chat_id, msg):
    user_id = msg['from']['id']
    first_name = msg['from']['first_name']
    last_name = msg['from']['last_name']
    username = msg['from']['username']
    bot.sendMessage(
        chat_id,
        language.wrong_id.format(user_id, username, first_name, last_name),
        reply_markup=remove_kb, parse_mode='Markdown')
    log.warning('Unauthorized access: ID {0} User:{1}, {2} {3} '.format(chat_id, username, first_name, last_name))


# noinspection PyGlobalUndefined
def _reply_wrong_command(chat_id, content):
    global got
    try:
        got = str(codecs.encode(content, 'utf-8')).replace('b', '').title()
        raise Exception('Not allowed input: ' + got)
    except Exception as ex:
        bot.sendMessage(chat_id, language.not_allowed, parse_mode='MarkdownV2')
        log.error(str(ex))
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
        if (command.title() == commands[0].title()) or (command == ('/' + commands[0])):
            bot.sendMessage(
                chat_id, language.pls_select.format(msg['from']['first_name']),
                reply_markup=functions_kb_markup, parse_mode='Markdown')
        # stop if command starts with 'stop' or '/stop'
        elif (command.title().startswith(commands[7].title())) or (command.startswith('/' + commands[7])):
            stop_threads()
            bot.sendMessage(
                chat_id, language.pls_select.format(msg['from']['first_name']),
                reply_markup=functions_kb_markup, parse_mode='Markdown')
        # all others
        elif any(c for c in commands if (command.title()) == (c.title())):
            bot.sendMessage(
                chat_id, '*' + command.title() + language.called, reply_markup=_stop_kb(command), parse_mode='Markdown')
            run_thread(command)
        else:
            _reply_wrong_command(chat_id, command)
    else:
        _reply_wrong_command(chat_id, content_type)


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
