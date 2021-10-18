#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "To make sure that only one bot instance is running, " \
          "bot class is subclass of Singleton!"

from telegram import ParseMode, Update
from telegram import ReplyKeyboardMarkup as telegram_ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove as telegram_ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, \
    MessageHandler, Filters

from clss import Singleton
from config import \
    token, access, \
    commands, \
    m_wrong_id, m_pls_select, m_not_allowed, m_started, m_rebooted, \
    m_stopped, m_updated, \
    AUTO_REBOOT_ENABLED, AUTO_REBOOT_CLOCK_TIME
from control import run_thread, stop_threads, service
from control.autoreboot import AutoReboot
from control.update import update_bot
from logger import LOGGER

RUNNING = "Bot is running..."
admins = [access.thk]


class TelegramBot(Singleton):
    """ Bot class using telegram framework
        (https://python-telegram-bot.org),
        Python >= 3
    """

    def __init__(self, t, ids):
        """
        :param t: bot token
        :param ids: allowed chat ids

        :type t: str
        :type ids: list of int
        """
        self.__token = t
        self.__admins = ids
        self.__logger = LOGGER
        self.__logger.debug(
            f"Initialize instance of {self.__class__.__name__}")

        self.__logger.debug(f"Building keyboards....")
        self._remove_keyboard = telegram_ReplyKeyboardRemove()
        self.__buttons = [
            [commands[2], commands[3], commands[6], commands[7],
             commands[16]],
            [commands[4], commands[5], commands[17], commands[18],
             commands[19]],
            [commands[15], commands[20]],
            [commands[8], commands[9], commands[10], commands[13],
             commands[11], commands[12], commands[14]]]
        self.__keyboard_markup = telegram_ReplyKeyboardMarkup(
            self.__buttons,
            resize_keyboard=True
        )
        self.__services = [service.NAME.lower(),
                           service.Service.c_info.replace('/', ''),
                           service.Service.c_help.replace('/', ''),
                           service.Service.c_reboot.replace('/', ''),
                           service.Service.c_update.replace('/', '')]
        self.__updater = Updater(self.__token, use_context=True)
        self.__dispatcher = self.__updater.dispatcher
        self.__bot = self.__updater.bot
        self.__start_handler = CommandHandler('start', self.__start)
        self.__stop_handler = CommandHandler('stop', self.__stop)
        self.__help_handler = CommandHandler('help', self.__help)
        self.__service_handler = CommandHandler(self.__services,
                                                self.__service)
        self.__commands_handler = MessageHandler(Filters.text(commands),
                                                 self.__handle)
        self.__func_thread = None

    def start(self):
        self.__dispatcher.add_error_handler(self.__error)
        self.__dispatcher.add_handler(self.__start_handler)
        self.__dispatcher.add_handler(self.__help_handler)
        self.__dispatcher.add_handler(self.__stop_handler)
        self.__dispatcher.add_handler(self.__service_handler)
        self.__dispatcher.add_handler(self.__commands_handler)

        if AUTO_REBOOT_ENABLED:
            AutoReboot(hour=AUTO_REBOOT_CLOCK_TIME, bot=self.__bot).start()
        self.__logger.info(f"Auto reboot enabled = {AUTO_REBOOT_ENABLED}")

        self.__updater.start_polling()
        self.__logger.info(RUNNING)
        for a in self.__admins:
            self.__logger.debug(
                f"Inform Admin '{a}' by message that bot is running.")
            self.__bot.send_message(a, m_started,
                                    reply_markup=self.rm_kb)
        self.__updater.idle()

    @property
    def rm_kb(self):
        return self._remove_keyboard

    @property
    def kb_markup(self):
        return self.__keyboard_markup

    @property
    def kb_stop(self):
        r = telegram_ReplyKeyboardMarkup([[commands[0]]])
        self.__logger.debug(f"Stop keyboard markup: {r}")
        return r

    @classmethod
    def external_request(cls, msg, chat_id=None, reply_markup=None, bot=None):
        if chat_id is None:
            for admin in bot.__admins:
                bot.__bot.send_message(admin, msg, reply_markup=reply_markup)
        else:
            bot.__bot.send_message(chat_id, msg, reply_markup=reply_markup)

    def __service(self, update: Update, context: CallbackContext):
        command = self.__get_command(update)
        # /service
        if command == ('/' + service.NAME.lower()):
            if self.__stop_function(update, context):
                self.__reply(update, service.menu, markup=self.rm_kb)
        elif command == service.Service.c_reboot:
            self.__reply(update, m_rebooted, markup=self.rm_kb)
        elif command == service.Service.c_info:
            if self.__stop_function(update, context):
                info = service.system_info()
                self.__reply(update, info, markup=self.rm_kb)
                self.__logger.info(info.replace("\n", "").replace(" ", ""))
        elif command == service.Service.c_update:
            if self.__stop_function(update, context):
                self.__reply(update, m_updated, markup=self.rm_kb)
                update_bot(m_updated)
        return

    def __help(self, update: Update, context: CallbackContext):
        self.__get_command(update)
        if self.__stop_function(update, context):
            self.__reply(update, service.get_help_text(), markup=self.rm_kb)
        return

    # noinspection PyMethodMayBeStatic
    def __reply(self, update: Update, text, markup=None):
        if markup is None:
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        else:
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN,
                                      reply_markup=markup)
        self.__logger.debug(update.message)
        return

    def __error(self, update: Update, context: CallbackContext):
        try:
            self.__logger.error(
                f"Update \"{update}\"\n"
                f"caused error \"{context.error}\"")
        except KeyboardInterrupt:
            self.__logger.warning('Program interrupted')
            exit()
        except Exception as e:
            self.__logger.warning('Any error occurs!', e)
            exit()

    def __stop(self, update: Update, context: CallbackContext):
        if self.__stop_function(update, context):
            self.__reply(update, m_stopped, markup=self.rm_kb)
        self.__logger.info("Bot stopped,  got '/stop'!")

    # noinspection PyUnusedLocal
    def __stop_function(self, update: Update, context: CallbackContext,
                        msg=None):
        if msg is not None:
            self.__reply(update, text=msg, markup=self.rm_kb)
        return True if stop_threads() else False

    def __start(self, update: Update, context: CallbackContext):
        last_name = update.message.from_user.last_name
        first_name = update.message.from_user.first_name
        username = update.message.from_user.username
        try:
            user_id = update.message.from_user.id
        except (NameError, AttributeError):
            try:
                user_id = update.inline_query.from_user.id
            except (NameError, AttributeError):
                try:
                    user_id = update.chosen_inline_result.from_user.id
                except (NameError, AttributeError):
                    try:
                        user_id = update.callback_query.from_user.id
                    except (NameError, AttributeError):
                        return exit()

        if user_id not in self.__admins:
            self.__logger.warning(
                f"Not allowed access by: {user_id} - {last_name},{first_name}")
            self.__reply(update,
                         m_wrong_id.format(user_id, username, first_name,
                                           last_name))

        else:
            self.__get_command(update)
            if self.__stop_function(update, context):
                self.__reply(update, text=m_pls_select.format(first_name),
                             markup=self.kb_markup)
                self.__logger.info(
                    f"Bot started: {user_id} - {last_name}, {first_name}")
                return

    # noinspection PyUnusedLocal
    def __handle(self, update: Update, context: CallbackContext):
        command = self.__get_command(update)
        # stop function
        if (command.startswith(commands[0])) \
                or (command.startswith(commands[0].lower())):
            if self.__stop_function(update, context):
                self.__reply(update,
                             m_pls_select.format(
                                 update.message.from_user.first_name),
                             markup=self.kb_markup)

        # all other commands
        elif any(c for c in commands if (command == c)):
            if self.__stop_function(update, context):
                self.__func_thread = run_thread(command,
                                                update.message.from_user.id,
                                                self)
                self.__reply(update, text=command, markup=self.kb_stop)

        else:
            return

    def __get_command(self, update):
        command = update.message.text
        self.__logger.info(f"Got command '{command}'")
        return command

    def __reply_wrong_command(self, update, command):
        try:
            raise Exception(f'Not allowed input: {command}')
        except Exception as ex:
            self.__reply(update, text=m_not_allowed, markup=None)
            self.__logger.warning(str(ex))
        return


def main():
    TelegramBot(token, admins).start()


if __name__ == '__main__':
    main()
