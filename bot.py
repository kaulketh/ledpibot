#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import time

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import config
import functions
import logger
from config.commands import commands
from functions import cancel

log = logger.get_logger('LedPiBot')

assert isinstance(config.token, str)
bot = telepot.Bot(config.token)
answerer = telepot.helper.Answerer(bot)
command = None

kb_markup = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=commands[1].title()), KeyboardButton(text=commands[2].title()),
     KeyboardButton(text=commands[3].title())],
    [KeyboardButton(text=commands[4].title()), KeyboardButton(text=commands[5].title()),
     KeyboardButton(text=commands[6].title())],
    [KeyboardButton(text=commands[7].title())],
    [KeyboardButton(text=commands[8].title())],
])

remove_kb = ReplyKeyboardRemove()


def on_chat_message(msg):
    global command
    content_type, chat_type, chat_id = telepot.glance(msg)
    log.debug('msg: {0} '.format(msg))

    if content_type is not 'text':
        reply_wrong_command(chat_id, content_type)
    else:
        command = msg['text']
    # start
    if (command == commands[0].title()) or (command == ('/' + commands[0])):
        bot.sendMessage(
            chat_id, '_Select a choice!_', reply_markup=kb_markup, parse_mode='Markdown')
    # cancel
    elif command == commands[7].title():
        cancel.pause_threads()
        bot.sendMessage(
            chat_id, '_Canceled!_\n_Try another choice._', reply_markup=kb_markup, parse_mode='Markdown')
    # stop
    elif (command == commands[8].title()) or (command == ('/' + commands[8])):
        cancel.stop_threads()
        bot.sendMessage(
            chat_id, '*Stopped!*', reply_markup=remove_kb, parse_mode='Markdown')
    # all others
    elif any(c for c in commands if (command.title()) == (c.title())):
        getattr(functions, command.replace(" ", "").lower()).run_thread()
        bot.sendMessage(chat_id, '*_' + command.title() + '_* called',
                        reply_markup=kb_markup, parse_mode='MarkdownV2')
    else:
        reply_wrong_command(chat_id, command)
    log.info('Command = ' + command)


def reply_wrong_command(chat_id, content):
    log.warning('Got wrong input: ' + content.title())
    try:
        bot.sendMessage(
            chat_id, '*_ ' + content.title() + '_*  is not allowed\\!', parse_mode='MarkdownV2')
    except Exception as ex:
        bot.sendMessage(chat_id, "*_Forbidden\\!_*".upper(), parse_mode='MarkdownV2')
        log.error("An error occurs: " + str(ex))
    # select a choice
    global command
    command = commands[0].title()


MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
log.debug('Bot is listening ...')
while 1:

    try:
        time.sleep(5)

    except KeyboardInterrupt:
        log.warning('Program interrupted')
        exit()

    except Exception as e:
        log.error('An error occurs: ' + str(e))
