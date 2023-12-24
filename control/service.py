#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os
import subprocess

from logger import LOGGER

GIT_API_URL = "https://api.github.com/repos/kaulketh/ledpibot"
NAME = "Service"

# [skip pep8] ignore=E501
# noinspection LongLine
# noinspection PyPep8
HELP_TEXT: str = """
*Manual*
- After boot bot will inform user that it is ready to use via message
- Use in-app command /start to start
- Bot welcomes the user
- Select any function/color to run
- Bot answers with called function
- Keyboard changes to stop-button keyboard
- User is able to stop the running function

It is possible to call in-app commands at any time!
*Call of any in-app command will break running function!*

- *Functions/Animations:*
    Clock 1:    One LED per 'watch hand', red hour hand, blue minute hand, warm yellow running second hand every 2.5 seconds.
    Clock 2:    One LED per 'watch hand', red hour, blue minute, blue running light every 2.5 minutes from the current 'minute' to the '12'.
    Clock 3:    One LED per 'watch hand', red hour, blue minute, green seconds 'scale' will extend every 2.5 seconds. There is also a 'dial', subtly warm yellow for each 'number'.
    Clock 4:    Colorful, full color 'watch face' for minute, hour, second, 'scales' will be overridden and colors mixed/changed thus.
    Clock 5:    Red hour hand, blue minute hand and warm yellow second 'pendulum' over all LEDs.
    Clock 6:    Similar Clock 4, but w/o seconds and Green and Blue as major colors.
    Clock 7:    White minute hand from LED 1 to 12 in 5 min steps (right half of circle), blue hour hand from LED 12 to 24 (left half of circle)
    Red, blue, green, white, yellow, orange, violet:    All LEDs at once can switched to same color.
    Colors:     Switching simple colors in random time periods.
    Colors II:  Fading over simple colors in random time periods.
    Rainbow:    Rainbow animation with circular fading effect.
    Rainbow II: Rainbow animation with chaser, included fading effect.
    Theater:    Extremely colorful animation with spinning and wiping effects.
    Theater II: Another colorful animation with spinning effects.
    Advent:     Advent calendar, works in Advent time only! For every day of December will one LED flicker like a candlelight. If it is Advent Sunday it flickers red. Should be time before December but in Advent period all LEDs are working as candle light. If it is other than Advent time LEDs will circle in orange as warning!
    Candles:    Each LED simulates candlelight.
    Strobe:     Emitting brief and rapid flashes of white light in random frequency.

- *Service* menu:
    /Reboot device
    /Restart bot application (running as service)
    /Info   Information commit/release versions on GitHub, host name, IP, memory usage, disk usage, cpu load.
    /Update Force update from GitHub to the latest version of master branch.
    /Help   This menu"""


class Service:
    c_prefix = "- "
    c_info = "/Info"
    c_reboot = "/Reboot"
    c_restart = "/Restart"
    c_update = "/Update"
    c_help = "/Help"

    def __init__(self, command: str = None, log_msg: str = None):
        self.__logger = LOGGER
        self.__log_msg = log_msg
        self.__command = command
        self.__help_txt = HELP_TEXT
        self.__menu_header = f"*{NAME}*:"
        self.__menu_dictionary = {
            0: self.c_reboot,
            1: self.c_restart,
            2: self.c_info,
            3: self.c_update,
            4: self.c_help
        }

        self.__new_line = "\n"
        self.__empty = ""

    def execute_os_command(self):
        if self.__command is not None:
            try:
                if self.__log_msg is not None:
                    self.__logger.info(self.__log_msg)
                else:
                    self.__logger.info(self.__command)
                os.system(self.__command)
            except Exception as e:
                self.__logger.error(f"{e}")
        else:
            raise Exception("No executable command found!")

    @property
    def menu(self):
        try:
            m = f"{self.__menu_header}{self.__new_line}"
            for key in self.__menu_dictionary.keys():
                line = f"{self.c_prefix}" \
                       f"{self.__menu_dictionary.get(key)}" \
                       f"{self.__new_line}"
                m += line
                self.__logger.debug(
                    f"add {line.replace(self.__new_line, self.__empty)}")
            return m
        except Exception as e:
            self.__logger.error(f"{e}")

    @property
    def help_text(self):
        return f"\n{self.__help_txt}"

    @property
    def system_info(self):
        try:
            host = subprocess.check_output("hostname", shell=True).upper()
            ip = "IP :  " + str(
                subprocess.check_output("hostname -I | cut -d\' \' -f1",
                                        shell=True))
            m = subprocess.check_output(
                "free -m | awk 'NR==2{printf \""
                "Memory :  %s / %s MB (%.0f%%)\", $3,$2,$3*100/$2 }'",
                shell=True)
            d = subprocess.check_output(
                "df -h | awk '$NF==\"/\"{printf \""
                "Disk :  %d / %d GB (%s)\", $3,$2,$5}'",
                shell=True)
            c = subprocess.check_output(
                "top - bn1 | grep \"Cpu(s)\""
                " | sed \"s/.*, *\\([0-9.]*\\)%* id.*/\\1/\" | "
                "awk '{print \"CPU Load :  \"100 - $1\"%\"}'", shell=True)
            return f"{host} " \
                   f"{self.__latest_release()} " \
                   f"({self.__latest_commit()}){self.__new_line}" \
                   f"{ip}{self.__new_line}" \
                   f"{m}{self.__new_line}" \
                   f"{d}{self.__new_line}" \
                   f"{c}" \
                .replace("b'", "").replace("'", "").replace("\\n", "")
        except Exception as e:
            self.__logger.error(f"{e}")

    @staticmethod
    def __latest_commit():
        commit = f"curl -s {GIT_API_URL}/commits/master --insecure "
        latest_com = f"{subprocess.check_output(commit, shell=True)[12:46]}" \
                     f"".replace("b'", "").replace("'", "").replace("\\n", "")
        commit_url_text = f"[{latest_com[0:7]}]" \
                          f"(https://github.com/kaulketh/ledpibot/commit/" \
                          f"{latest_com})"
        return commit_url_text

    @staticmethod
    def __latest_release():
        release = f"curl -s {GIT_API_URL}/releases/latest --insecure |" \
                  " grep -Po '\"tag_name\": \"\\K.*?(?=\")'"
        return f"{subprocess.check_output(release, shell=True)}" \
            .replace("b'", "").replace("'", "").replace("\\n", "")


def reboot_device(log_msg: str = None):
    Service("sudo reboot", log_msg).execute_os_command()


def restart_service(log_msg: str = None):
    Service("sudo systemctl restart ledpibot.service",
            log_msg).execute_os_command()


def system_info():
    return Service().system_info


def get_help_text():
    return Service().help_text


def service_menu():
    return Service().menu


menu = service_menu()

if __name__ == '__main__':
    pass
