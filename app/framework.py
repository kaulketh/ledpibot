#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import codecs
import datetime
import signal
import traceback

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove

# noinspection PyUnresolvedReferences
from config import auto_reboot, auto_reboot_time, ID_CHAT_THK, \
    running, TOKEN_TELEGRAM_BOT, commands, m_not_allowed, m_pls_select, \
    m_rebooted, m_restarted, m_started, m_stopped, m_updated, m_wrong_id, \
    auto_start, auto_reboot_msg, auto_start_msg
from control import peripheral_functions, run_thread, service, \
    stop_threads
from control.reboot import AutoReboot
from control.update import update_bot
from functions import indices_of_functions, STOP, START
from logger import LOGGER, HISTORY

admins = [ID_CHAT_THK]


class TelepotBot:
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
        self.__log.debug(
            f"Initialize instance of {self.__class__.__name__} {self}")
        self.__token = t
        self.__admins = ids
        self.__bot = telepot.Bot(self.__token)

        # keyboards and buttons arrangement (refer config)
        self.__rm_kb = ReplyKeyboardRemove()
        self.__kb = []
        for i in range(len(indices_of_functions)):
            self.__kb.append(self.__btn_grp(indices_of_functions[i]))
        self.__kbm = ReplyKeyboardMarkup(keyboard=self.__kb)
        self.__log.debug(f"Done, keyboards and buttons built.")
        self.__func_thread = None

    @property
    def kb_stop(self) -> ReplyKeyboardMarkup:
        self.__log.debug("Init Stop keyboard")
        return ReplyKeyboardMarkup(keyboard=[[self.__btn(STOP, 0)]])

    @classmethod
    def external_request(cls, msg, chat_id=None, reply_markup=None, bot=None):
        if chat_id is None:
            for admin in bot.__admins:
                bot.__send(admin, text=msg, reply_markup=reply_markup)
        else:
            bot.__send(ch_id=chat_id, text=msg, reply_markup=reply_markup)

    # noinspection PyMethodMayBeStatic
    def __btn(self, text, i) -> KeyboardButton:
        self.__log.debug(f"[{i:02d}] {text}")
        return KeyboardButton(text=text)

    # noinspection PyMethodMayBeStatic
    def __btn_grp(self, choices: list) -> list:
        btn_list, il = [], []
        for i in choices:
            btn_list.append(self.__btn(commands[i], i))
            il.append(i)
        self.__log.debug(f"{il} arranged")
        return btn_list

    def __send(self, ch_id, text, reply_markup, parse_mode='Markdown'):
        self.__log.info(text.split(sep='/n'))
        self.__bot.sendMessage(ch_id, text, reply_markup=reply_markup,
                               parse_mode=parse_mode)

    # noinspection PyMethodMayBeStatic
    def __user(self, msg):
        user_id = msg['from']['id']
        first_name = msg['from']['first_name']
        last_name = msg['from']['last_name']
        username = msg['from']['username'] if (
                'username' in msg['from'].keys()) else "'user name unknown'"
        return user_id, username, first_name, last_name

    def __reply_wrong_id(self, ch_id, msg):
        try:
            uid, nick, first, last = self.__user(msg)
            log_msg = f"Unauthorized access: ID " \
                      f"{ch_id} User:{nick}, {first} {last}"
            self.__send(ch_id, m_wrong_id.format(uid, nick, first, last),
                        reply_markup=self.__rm_kb)
            raise Exception(log_msg)
        except Exception as ex:
            self.__log.warning(f"{ex}")

    def __reply_wrong_content(self, ch_id, content):
        try:
            got = str(codecs.encode(content, 'utf-8')).replace('b', '')
            raise Exception(f'Not allowed input: {got}')
        except Exception as ex:
            self.__send(ch_id, m_not_allowed, parse_mode='MarkdownV2',
                        reply_markup=None)
            self.__log.warning(str(ex))
        return

    def __stop_function(self, ch_id, msg) -> bool:
        if msg is not None:
            self.__send(ch_id, msg, reply_markup=self.__rm_kb)
        return stop_threads()

    def __handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        command = msg['text']
        self.__log.debug(msg)

        # helper
        def respond(txt):
            self.__send(chat_id, txt, reply_markup=self.__rm_kb)

        def selection_ok(selection) -> bool:
            return command == selection and self.__stop_function(chat_id,
                                                                 msg=None)

        def request_selection():
            self.__send(chat_id, m_pls_select.format(self.__user(msg)[2]),
                        reply_markup=self.__kbm)

        help_requested = (selection_ok(service.Service.c_help) or
                          selection_ok(service.Service.c_help.lower()))

        sos = (command.startswith(STOP) or
               command.startswith(STOP.lower()) or
               command.startswith(START) or
               command.startswith(START.lower()))

        # check user
        if chat_id not in self.__admins:
            self.__reply_wrong_id(chat_id, msg)
            uid, nick, first, last = self.__user(msg)
            m = f"{msg['text']} -> {chat_id}, {uid} {nick}, {first} {last}"
            self.external_request(msg=m, chat_id=ID_CHAT_THK, bot=self)
            return None

        # check content
        if content_type == 'text':
            self.__log.info(command)
            # Bot menu respectively Telegram-in-app-commands
            if selection_ok("/start"):
                request_selection()
            elif selection_ok("/stop"):
                respond(m_stopped)
            elif selection_ok('/' + service.NAME.lower()):
                respond(service.menu)
            elif selection_ok(service.Service.c_reboot):
                respond(m_rebooted)
                service.reboot_device(m_rebooted)
            elif selection_ok(service.Service.c_restart):
                respond(m_restarted)
                service.restart_service(m_restarted)
            elif selection_ok(service.Service.c_info):
                info = service.system_info()
                respond(info)
                self.__log.info(info.replace("\n", "").replace(" ", ""))
            elif selection_ok(service.Service.c_update):
                respond(m_updated)
                update_bot(m_updated)
            elif help_requested:
                respond(service.get_help_text())
            # start or stop w/o leading '/'
            elif sos:
                if self.__stop_function(chat_id, msg=None):
                    request_selection()
            # all other commands
            elif any(c for c in commands if (selection_ok(c))):
                self.__func_thread = run_thread(command, chat_id, self)
                self.__send(chat_id, text=command, reply_markup=self.kb_stop)
            else:
                # wrong command
                self.__reply_wrong_content(chat_id, command)
        else:
            # wrong type
            self.__reply_wrong_content(chat_id, content_type)

    def start(self):
        # welcome and run
        self.__log.debug(running)
        for a in self.__admins:
            self.__send(a, m_started, reply_markup=self.__rm_kb)
        MessageLoop(self.__bot, {'chat': self.__handle}).run_as_thread()

        # TODO: implement considering of translation of
        #  stored command after language change
        #  e.g. search key of value/stored string and gather
        #  translations with this key, depending of set language
        #  and execute/set command text

        # history check
        first_line = "new file"
        try:  # file check
            with open(HISTORY, "r") as f:
                lines = f.readlines()
                if lines:
                    pass
                else:
                    raise ValueError("Empty file")
        except (FileNotFoundError, ValueError):
            # new empty file
            with open(HISTORY, "w") as f:
                f.write(f"{first_line}\n")
            with open(HISTORY, "r") as f:
                lines = f.readlines()
        line = lines[-1]
        self.__log.debug(line.strip())
        cmd = line.partition(" HISTORY ")[2].rstrip()

        # check autostart and run stored function
        new_file = lines[0].startswith(first_line)
        stop_stored = cmd == STOP
        if auto_start:
            log = f"{auto_start_msg}: {cmd}"
            if stop_stored or new_file:
                kbm = self.__kbm if not auto_reboot else None
                m = m_pls_select.replace(",", "").replace(" {0}", "")
                open(HISTORY, "w").close()
                self.__send(ID_CHAT_THK, m, reply_markup=kbm)
            else:
                self.__func_thread = run_thread(cmd, ID_CHAT_THK, self)
                for a in self.__admins:
                    self.__send(a, log, reply_markup=self.kb_stop)
            self.__log.info(log)

        # auto reboot check and initializing
        if auto_reboot:
            self.__log.info(auto_reboot_msg)
            for a in self.__admins:
                if auto_start and stop_stored:
                    m = self.__kbm
                elif auto_start and not stop_stored:
                    m = self.kb_stop
                else:
                    m = self.__rm_kb
                self.__send(a, f"{auto_reboot_msg}: "
                               f"{auto_reboot_time}"
                               f":{datetime.datetime.now().second:02d} "
                               f"CET",
                            reply_markup=m)
            AutoReboot(reboot_time=auto_reboot_time, bot=self).start()

        # main loop
        while True:
            try:
                signal.pause()
            except KeyboardInterrupt:
                self.__log.warning('Program interrupted')
                exit()
            except Exception as e:
                self.__log.error(f"Any error occurs: {traceback.format_exc()}")
                self.__log.exception(e)
                exit()
            finally:
                peripheral_functions.get(3)()


def main():
    TelepotBot(TOKEN_TELEGRAM_BOT, admins).start()


if __name__ == '__main__':
    pass
