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
from config.commands import Commands
from functions import cancel

log = logger.get_logger('LedPiBot')

assert isinstance(config.token, str)
bot = telepot.Bot(config.token)
answerer = telepot.helper.Answerer(bot)

kb_markup = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text=Commands.advent.name.upper()), KeyboardButton(text=Commands.animation.name.upper())],
            [KeyboardButton(text=Commands.clock.name.upper()), KeyboardButton(text=Commands.xmas.name.upper())],
            [KeyboardButton(text=Commands.cancel.name.upper())],
            [KeyboardButton(text=Commands.stop.name.upper())],
        ])

remove_kb = ReplyKeyboardRemove()


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # TODO: adapt message content
    log.info('msg: {0} '.format(msg))

    command = msg['text'].lower()

    if (command == Commands.start.name) or (command == ('/' + Commands.start.name)):
        bot.sendMessage(
            chat_id, '_Select a choice_', reply_markup=kb_markup, parse_mode='Markdown')

    elif (command == Commands.stop.name) or (command == ('/' + Commands.stop.name)):
        cancel.stop_threads()
        bot.sendMessage(
            chat_id, '*Stopped!*', reply_markup=remove_kb, parse_mode='Markdown')

    elif command == Commands.cancel.name:
        cancel.pause_threads()
        bot.sendMessage(
            chat_id, '*Function canceled!*\n*Try another choice.*', reply_markup=kb_markup, parse_mode='Markdown')

    elif any(c for c in Commands if command == c.name):
        getattr(functions, command).run_thread()
        bot.sendMessage(chat_id, '_' + command.upper() + '_ called', reply_markup=kb_markup, parse_mode='Markdown')

    else:
        log.warning('Got wrong input: ' + command)
        bot.sendMessage(
            chat_id, '*' + command.upper() + '* is not allowed!', reply_markup=remove_kb, parse_mode='Markdown')

    log.info('Got command: ' + command.upper())


MessageLoop(bot, {'chat': on_chat_message}).run_as_thread()
log.debug('Bot is listening ...')
while 1:

    # noinspection PyBroadException
    try:
        time.sleep(5)

    except KeyboardInterrupt:
        log.warning('Program interrupted')
        exit()

    except Exception:
        log.error('Any error occurs')
