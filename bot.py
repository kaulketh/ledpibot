#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import codecs
import signal

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from config import \
    token, access, \
    commands, \
    wrong_id, pls_select, not_allowed, called, started, rebooted, stopped, stop_msg, updated, \
    AUTO_REBOOT_ENABLED, AUTO_REBOOT_CLOCK_TIME
from control import run_thread, stop_threads, service
from control.autoreboot import AutoReboot
from control.update import update_bot
from logger import LOGGER

BOT = telepot.Bot(token)

admins = [access.thk, access.annib]

# region Keyboards
stop = commands[0]
start = commands[1]


def btn(text):
    return KeyboardButton(text=text)


kb_markup = ReplyKeyboardMarkup(keyboard=[
    [btn(commands[2]), btn(commands[3]), btn(commands[6]), btn(commands[7]), btn(commands[16])],
    [btn(commands[4]), btn(commands[5]), btn(commands[17]), btn(commands[18]), btn(commands[19])],
    [btn(commands[15]), btn(commands[20])],
    [btn(commands[8]), btn(commands[9]), btn(commands[10]),
     btn(commands[13]), btn(commands[11]), btn(commands[12]), btn(commands[14])]
])

rm_kb = ReplyKeyboardRemove()


def kb_stop(func=None):
    return ReplyKeyboardMarkup(keyboard=[[btn(stop)]]) \
        if func is None else ReplyKeyboardMarkup(keyboard=[[btn(stop + '\"' + func + '\"')]])


# endregion

# region Methods
# noinspection PyShadowingNames
def send(chat_id, text, reply_markup=kb_markup, parse_mode='Markdown'):
    LOGGER.debug(f"Message posted: {chat_id}|{text}|{reply_markup}|{parse_mode}".replace("\n", " "))
    return BOT.sendMessage(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)


# noinspection PyShadowingNames
def reply_wrong_id(chat_id, msg):
    user_id = msg['from']['id']
    first_name = msg['from']['first_name']
    last_name = msg['from']['last_name']
    username = msg['from']['username']
    log_msg = f"Unauthorized access: ID {chat_id} User:{username}, {first_name} {last_name}"
    send(chat_id, wrong_id.format(user_id, username, first_name, last_name), reply_markup=rm_kb)
    send(f"Attention! {access.thk}", log_msg)
    LOGGER.warning(log_msg)


# noinspection PyShadowingNames
def reply_wrong_command(chat_id, content):
    try:
        got = str(codecs.encode(content, 'utf-8')).replace('b', '')
        raise Exception(f'Not allowed input: {got}')
    except Exception as ex:
        send(chat_id, not_allowed, parse_mode='MarkdownV2')
        LOGGER.warning(str(ex))
    return


# noinspection PyShadowingNames
def stop_function(chat_id, msg=stop_msg):
    if msg is not None:
        send(chat_id, msg, reply_markup=rm_kb)
    return True if stop_threads() else False


# noinspection PyGlobalUndefined
def handle(msg):
    global command, chat_id
    content_type, chat_type, chat_id = telepot.glance(msg)
    LOGGER.debug(msg)

    # check user
    if chat_id not in admins:
        reply_wrong_id(chat_id, msg)
        return

    if content_type == 'text':
        command = msg['text']
        LOGGER.info(f'Requested: {command}')
        # /start
        if command == "/start":
            send(chat_id, pls_select.format(msg['from']['first_name']))

        # /stop
        elif command == "/stop":
            if stop_function(chat_id, msg=None):
                send(chat_id, stopped, reply_markup=rm_kb)

        # stop function
        elif (command.startswith(stop)) or (command.startswith(stop.lower())):
            if stop_function(chat_id, msg=None):
                send(chat_id, pls_select.format(msg['from']['first_name']))

        # /service
        elif command == ('/' + service.NAME.lower()):
            if stop_function(chat_id):
                send(chat_id, service.menu, reply_markup=rm_kb)
        elif command == service.OSCommand.c_reboot:
            send(chat_id, rebooted, reply_markup=rm_kb)
            service.reboot_device(rebooted)
        elif command == service.OSCommand.c_system:
            send(chat_id, service.system_info(), reply_markup=rm_kb)
            LOGGER.info(service.system_info().replace("\n", " "))
        elif command == service.OSCommand.c_update:
            send(chat_id, updated, reply_markup=rm_kb)
            update_bot(updated)
        # all other commands
        elif any(c for c in commands if (command == c)):
            if stop_function(chat_id, msg=None):
                send(chat_id, called.format(command), reply_markup=kb_stop(), parse_mode='MarkdownV2')
                run_thread(command, chat_id)
        else:
            reply_wrong_command(chat_id, command)
    else:
        reply_wrong_command(chat_id, content_type)


# noinspection PyShadowingNames
def external_request(msg, chat_id=None, reply_markup=None):
    if chat_id is None:
        for chat_id in admins:
            send(chat_id, msg, reply_markup)
    else:
        send(chat_id, msg, reply_markup)


def start_bot():
    LOGGER.info("Bot is running...")
    for admin in admins:
        send(admin, started, reply_markup=rm_kb)

    MessageLoop(BOT, {'chat': handle}).run_as_thread()
    if AUTO_REBOOT_ENABLED:
        AutoReboot(AUTO_REBOOT_CLOCK_TIME).start()

    while True:
        try:
            signal.pause()
        except KeyboardInterrupt:
            LOGGER.warning('Program interrupted')
            exit()
        except Exception as e:
            LOGGER.error(f"Any error occurs: {e}")
            exit()


# endregion
if __name__ == '__main__':
    start_bot()
