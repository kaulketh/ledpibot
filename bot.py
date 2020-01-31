#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import time
import codecs

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import config
import logger
from config.commands import commands
from control import run_thread, stop_threads

log = logger.get_logger('LedPiBot')

assert isinstance(config.token, str)
bot = telepot.Bot(config.token)
answerer = telepot.helper.Answerer(bot)
command = None

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


def __on_chat_message(msg):
    global command
    content_type, chat_type, chat_id = telepot.glance(msg)

    log.debug(msg)

    if content_type == 'text':
        command = msg['text']
        log.info('Command = ' + command)
        # start
        if (command.title() == commands[0].title()) or (command == ('/' + commands[0])):
            bot.sendMessage(
                chat_id, 'Please make a suitable selection!', reply_markup=functions_kb_markup, parse_mode='Markdown')
        # stop if command starts with 'stop' or '/stop'
        elif (command.title().startswith(commands[7].title())) or (command.title().startswith('/' + commands[7])):
            stop_threads()
            bot.sendMessage(
                chat_id, 'Please make a suitable selection!', reply_markup=functions_kb_markup, parse_mode='Markdown')
        # all others
        elif any(c for c in commands if (command.title()) == (c.title())):
            bot.sendMessage(
                chat_id, '*' + command.title() + '* called.', reply_markup=_stop_kb(command), parse_mode='Markdown')
            run_thread(command)
        else:
            __reply_wrong_command(chat_id, command)
    else:
        __reply_wrong_command(chat_id, content_type)


def __reply_wrong_command(chat_id, content):
    global got
    try:
        got = str(codecs.encode(content, 'utf-8')).replace('b', '').title()
        raise Exception('Not allowed input: ' + got)
    except Exception as ex:
        bot.sendMessage(chat_id, '* Not allowed for this bot\\! *', parse_mode='MarkdownV2')
        log.error(str(ex))
    return


MessageLoop(bot, {'chat': __on_chat_message}).run_as_thread()
log.debug('Bot is listening ...')
while 1:

    try:
        time.sleep(5)

    except KeyboardInterrupt:
        log.warning('Program interrupted')
        exit()

    except Exception as e:
        log.error('An error occurs: ' + str(e))
