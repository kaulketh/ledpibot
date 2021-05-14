#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "To make sure that only one bot instance is running, " \
          "bot class is subclass of Singleton!"

import codecs
import signal

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove

from clss import Singleton
from config import \
    token, access, \
    commands, \
    m_wrong_id, m_pls_select, m_not_allowed, m_called, \
    m_started, m_rebooted, m_stopped, m_updated, \
    AUTO_REBOOT_ENABLED, AUTO_REBOOT_CLOCK_TIME, \
    COUNTDOWN_DISPLAY_REMAINING_RUNTIME
from control import run_thread, stop_threads, service
from control.autoreboot import AutoReboot
from control.update import update_bot
from logger import LOGGER

RUNNING = "Bot is running..."
admins = [access.thk]


class TelepotBot(Singleton):
    """ Bot class using telepot framework
        (https://telepot.readthedocs.io),
        Python >= 3
    """

    def __init__(self, t, ids):
        """
        :param t: bot token
        :param ids: allowed chat ids

        :type t: str
        :type ids: list of int
        """
        self.__log = LOGGER
        self.__log.debug(f"Initialize instance of {self.__class__.__name__}")
        self.__token = t
        self.__admins = ids
        self.__bot = telepot.Bot(self.__token)

        self.__log.debug(f"Building keyboards....")
        self._remove_keyboard = ReplyKeyboardRemove()
        self.__keyboard_markup = ReplyKeyboardMarkup(keyboard=[
            self.__buttons([2, 3, 6, 7, 16]),
            self.__buttons([4, 5, 17, 18, 19]),
            self.__buttons([15, 20]),
            self.__buttons([8, 9, 10, 13, 11, 12, 14])
        ])
        self.__func_thread = None

    @property
    def rm_kb(self):
        return self._remove_keyboard

    @property
    def kb_markup(self):
        return self.__keyboard_markup

    @property
    def kb_stop(self):
        r = ReplyKeyboardMarkup(
            keyboard=[[self.__button(commands[0])]])
        self.__log.debug(f"Stop keyboard markup: {r}")
        return r

    @property
    def kb_stop_standby(self):
        r = ReplyKeyboardMarkup(
            keyboard=[
                [self.__button(commands[0])],
                [self.__button(commands[21])]
            ])
        self.__log.debug(f"Stop/Standby keyboard markup: {r}")
        return r

    @classmethod
    def external_request(cls, msg, chat_id=None, reply_markup=None, bot=None):
        if chat_id is None:
            for admin in bot.__admins:
                bot.__send(admin, text=msg, reply_markup=reply_markup)
        else:
            bot.__send(ch_id=chat_id, text=msg, reply_markup=reply_markup)

    def __button(self, text) -> KeyboardButton:
        self.__log.debug(f"Build button: {text}")
        return KeyboardButton(text=text)

    def __buttons(self, indices: list, command_list: list = commands) -> list:
        btn_list = []
        for i in indices:
            self.__log.debug(
                f"Build and append button to list: {command_list[i]}")
            btn_list.append(KeyboardButton(text=command_list[i]))
        self.__log.debug(f"Button list: {btn_list}")
        return btn_list

    def __send(self, ch_id, text, reply_markup, parse_mode='Markdown'):
        self.__log.debug(
            f"Message posted: "
            f"{ch_id}|{text}|{reply_markup}|{parse_mode}".replace("\n", " "))
        self.__bot.sendMessage(ch_id, text, reply_markup=reply_markup,
                               parse_mode=parse_mode)

    def __reply_wrong_id(self, ch_id, msg):
        try:
            user_id = msg['from']['id']
            first_name = msg['from']['first_name']
            last_name = msg['from']['last_name']
            username = msg['from']['username']
            log_msg = f"Unauthorized access: ID " \
                      f"{ch_id} User:{username}, {first_name} {last_name}"
            self.__send(ch_id, m_wrong_id.format(user_id, username, first_name,
                                                 last_name),
                        reply_markup=self.rm_kb)
            raise Exception(log_msg)
        except Exception as ex:
            self.__log.warning(f"{ex}")

    def __reply_wrong_command(self, ch_id, content):
        try:
            got = str(codecs.encode(content, 'utf-8')).replace('b', '')
            raise Exception(f'Not allowed input: {got}')
        except Exception as ex:
            self.__send(ch_id, m_not_allowed, parse_mode='MarkdownV2',
                        reply_markup=None)
            self.__log.warning(str(ex))
        return

    def __stop_function(self, ch_id, msg):
        if msg is not None:
            self.__send(ch_id, msg, reply_markup=self.rm_kb)
        return True if stop_threads() else False

    def __handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.__log.debug(msg)

        # check user
        if chat_id not in self.__admins:
            self.__reply_wrong_id(chat_id, msg)
            return None

        if content_type == 'text':
            command = msg['text']
            self.__log.info(f"Got command '{command}'")
            # /start
            if command == "/start":
                if self.__stop_function(chat_id, msg=None):
                    self.__send(chat_id,
                                m_pls_select.format(msg['from']['first_name']),
                                reply_markup=self.kb_markup)

            # /stop
            elif command == "/stop":
                if self.__stop_function(chat_id, msg=None):
                    self.__send(chat_id, m_stopped, reply_markup=self.rm_kb)

            # stop function
            elif (command.startswith(commands[0])) \
                    or (command.startswith(commands[0].lower())):
                if self.__stop_function(chat_id, msg=None):
                    self.__send(chat_id,
                                m_pls_select.format(msg['from']['first_name']),
                                reply_markup=self.kb_markup)
            # force standby
            elif command == commands[21]:
                self.__func_thread.force_standby()

            # /service
            elif command == ('/' + service.NAME.lower()):
                if self.__stop_function(chat_id, msg=None):
                    self.__send(chat_id, service.menu, reply_markup=self.rm_kb)
            elif command == service.Service.c_reboot:
                self.__send(chat_id, m_rebooted, reply_markup=self.rm_kb)
                service.reboot_device(m_rebooted)
            elif command == service.Service.c_info:
                if self.__stop_function(chat_id, msg=None):
                    info = service.system_info()
                    self.__send(chat_id, info, reply_markup=self.rm_kb)
                    self.__log.info(info.replace("\n", "").replace(" ", ""))
            elif command == service.Service.c_update:
                if self.__stop_function(chat_id, msg=None):
                    self.__send(chat_id, m_updated, reply_markup=self.rm_kb)
                    update_bot(m_updated)
            elif command == service.Service.c_help \
                    or command == service.Service.c_help.lower():
                if self.__stop_function(chat_id, msg=None):
                    self.__send(chat_id, service.get_help_text(),
                                reply_markup=self.rm_kb)

            # all other commands
            elif any(c for c in commands if (command == c)):
                if self.__stop_function(chat_id, msg=None):
                    self.__func_thread = run_thread(command, chat_id, self)
                    self.__send(
                        chat_id,
                        m_called.format(
                            command,
                            self.__func_thread.recalculated_time(
                                self.__func_thread.countdown_hours())),
                        reply_markup=self.kb_stop_standby,
                        parse_mode='MarkdownV2')
            else:
                self.__reply_wrong_command(chat_id, command)
        else:
            self.__reply_wrong_command(chat_id, content_type)

    def start(self):
        self.__log.info(RUNNING)
        for a in self.__admins:
            self.__send(a, m_started, reply_markup=self.rm_kb)
        MessageLoop(self.__bot,
                    {'chat': self.__handle}).run_as_thread()
        if AUTO_REBOOT_ENABLED:
            AutoReboot(hour=AUTO_REBOOT_CLOCK_TIME, bot=self).start()
        self.__log.info(f"Auto reboot enabled = {AUTO_REBOOT_ENABLED}")
        self.__log.info(f"Countdown display remaining time enabled = "
                        f"{COUNTDOWN_DISPLAY_REMAINING_RUNTIME}")
        while True:
            try:
                signal.pause()
            except KeyboardInterrupt:
                self.__log.warning('Program interrupted')
                exit()
            except Exception as e:
                self.__log.error(f"Any error occurs: {e}")
                exit()


def main():
    TelepotBot(token, admins).start()


if __name__ == '__main__':
    main()
