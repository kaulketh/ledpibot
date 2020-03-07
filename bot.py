#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import codecs
import signal

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import logger
from config import \
    token, access, \
    commands, \
    wrong_id, pls_select, not_allowed, called, started, rebooted, rotated, stopped, stop_msg, killed, updated
from control import run_thread, stop_threads, service

LOG = logger.get_logger('LedPiBot')
BOT = telepot.Bot(token)

admins = [access.thk, access.annib]

# region Keyboards
stop = commands[0]
start = commands[1]


def _btn(text):
    return KeyboardButton(text=text)


kb_markup = ReplyKeyboardMarkup(keyboard=[
    [_btn(commands[2]), _btn(commands[3]), _btn(commands[6]), _btn(commands[7]), _btn(commands[16])],
    [_btn(commands[4]), _btn(commands[5]), _btn(commands[17]), _btn(commands[18]), _btn(commands[19])],
    [_btn(commands[15]), _btn(commands[20])],
    [_btn(commands[8]), _btn(commands[9]), _btn(commands[10]),
     _btn(commands[13]), _btn(commands[11]), _btn(commands[12]), _btn(commands[14])]
])

rm_kb = ReplyKeyboardRemove()


def _kb_stop(func=None):
    if func is None:
        return ReplyKeyboardMarkup(keyboard=[[_btn(stop)]])
    else:
        return ReplyKeyboardMarkup(keyboard=[[_btn(stop + ' \"' + func + '\"')]])


# endregion

# region Methods
def _ready_to_use():
    LOG.info("Bot is running...")
    for admin in admins:
        _send(admin, started, reply_markup=rm_kb)


# noinspection PyShadowingNames
def _send(chat_id, text, reply_markup=kb_markup, parse_mode='Markdown'):
    LOG.debug(
        "Message posted: {0}|{1}|{2}|{3}".format(
            str(chat_id), text, str(reply_markup), str(parse_mode)).replace("\n", " "))
    return BOT.sendMessage(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)


# noinspection PyShadowingNames
def _reply_wrong_id(chat_id, msg):
    user_id = msg['from']['id']
    first_name = msg['from']['first_name']
    last_name = msg['from']['last_name']
    username = msg['from']['username']
    _send(chat_id, wrong_id.format(user_id, username, first_name, last_name), reply_markup=rm_kb)
    log_msg = 'Unauthorized access: ID {0} User:{1}, {2} {3} '.format(chat_id, username, first_name, last_name)
    _send("Attention! " + access.thk, log_msg)
    LOG.warning(log_msg)


# noinspection PyShadowingNames
def _reply_wrong_command(chat_id, content):
    try:
        got = str(codecs.encode(content, 'utf-8')).replace('b', '')
        raise Exception('Not allowed input: ' + got)
    except Exception as ex:
        _send(chat_id, not_allowed, parse_mode='MarkdownV2')
        LOG.warning(str(ex))
    return


# noinspection PyShadowingNames
def _stop(chat_id, msg=stop_msg):
    if msg is not None:
        _send(chat_id, msg, reply_markup=rm_kb)
    if stop_threads():
        return_bool = True
    else:
        return_bool = False
    return return_bool


# noinspection PyGlobalUndefined
def _on_chat_message(msg):
    global command, chat_id
    content_type, chat_type, chat_id = telepot.glance(msg)
    LOG.debug(msg)

    # check user
    if chat_id not in admins:
        _reply_wrong_id(chat_id, msg)
        return

    if content_type == 'text':
        command = msg['text']
        LOG.info('Requested: ' + command)
        # /start
        if command == "/start":
            _send(chat_id, pls_select.format(msg['from']['first_name']))

        # /stop
        elif command == "/stop":
            if _stop(chat_id, msg=None):
                _send(chat_id, stopped, reply_markup=rm_kb)

        # stop function
        elif (command.startswith(stop)) or (command.startswith(stop.lower())):
            if _stop(chat_id, msg=command):
                _send(chat_id, pls_select.format(msg['from']['first_name']))

        # /service
        elif command == ('/' + service.NAME.lower()):
            if _stop(chat_id):
                _send(chat_id, service.menu, reply_markup=rm_kb)
        elif command == service.c_rotate:
            service.log_rotate_bot(rotated)
            _send(chat_id, rotated, reply_markup=rm_kb)
        elif command == service.c_reboot:
            _send(chat_id, rebooted, reply_markup=rm_kb)
            service.reboot_device(rebooted)
        elif command == service.c_system:
            _send(chat_id, service.system_usage(), reply_markup=rm_kb)
            LOG.info(service.system_usage().replace("\n", " "))
        elif command == service.c_kill:
            _send(chat_id, killed, reply_markup=rm_kb)
            service.kill_bot(killed)
        elif command == service.c_update:
            _send(chat_id, updated, reply_markup=rm_kb)
            service.update_bot(updated)
        elif command == service.c_test:
            _test(chat_id, BOT)

        # all other commands
        elif any(c for c in commands if (command == c)):
            if _stop(chat_id, msg=None):
                _send(chat_id, called.format(command), reply_markup=_kb_stop(), parse_mode='MarkdownV2')
                run_thread(command)
        else:
            _reply_wrong_command(chat_id, command)
    else:
        _reply_wrong_command(chat_id, content_type)


# noinspection PyShadowingNames
def external_request(msg, chat_id=None):
    if chat_id is None:
        for chat_id in admins:
            _send(chat_id, msg)
    else:
        _send(chat_id, msg)


def start_bot():
    _ready_to_use()
    MessageLoop(BOT, {'chat': _on_chat_message}).run_as_thread()
    while True:
        try:
            signal.pause()
        except KeyboardInterrupt:
            LOG.warning('Program interrupted')
            exit()
        except Exception as e:
            LOG.error('An error occurs: ' + str(e))
            exit()


# noinspection PyShadowingNames,PyUnusedLocal
def _test(chat_id=None, bot=None):
    pass


# endregion
if __name__ == '__main__':
    start_bot()
