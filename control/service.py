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
HELP_TEXT: str = """
*Manual*
- After boot bot will inform user that it is ready to use via message
- Use in-app command /start to start
- Bot welcomes the user
- Select any function/color to run
- Bot messages about run and the clock time of auto-standby
- Keyboard changes to 2-button keyboard (stop/standby)
- User is able to stop the running function or to force standby
- Bot messages the clock time of restart
- When standby mode is reached only one stop button is displayed. User is able to break the running standby.

It is possible to call in-app commands at any time!
*Call of any in-app command will break running function!*

- *Functions/Animations:*
    Clock 1:    One LED per 'pointer', red hours 'pointer', blue minutes 'pointer', warm yellow running seconds 'pointer' every 2.5 seconds.
    Clock 2:    One LED per 'pointer', red hour, blue minute, lue running light every 2.5 minutes from the current 'minute' to the '12'.
    Clock 3:    One LED per 'pointer', red hour, blue minute, green seconds 'scale' will extends every 2.5 seconds. There is also a 'dial', subtly warm yellow for each 'number'.
    Clock 4:    Colorful, full color 'scale' for minute, hour, second, 'scales' will overridden and colors mixed/changed thus.
    Clock 5:    Red hours 'pointer', blue minutes 'pointer' and warm yellow second 'pendulum' over all LEDs.
    Advent:     Advent calendar, works in December only! For every day of December will one LED flicker like a candle light. If it is Advent Sunday it flickers red. If it is other than December all LEDs will be flickering in red as warning!
    Candles:    Each LED simulates candle light.
    Rainbow:    Rainbow animation with circular fading effect.
    Theater:    Extremely colorful animation with chaser, spinning and wiping effects.
    Strobe:     Emitting brief and rapid flashes of white light in random frequency.
    Colors:     Switching simple colors in random time periods.
    Colors 2:   Fading over simple colors in random time periods.
    Red, blue, green, white, yellow, orange, violet:    All LEDs at once can switched to same color.

- *Service menu:*
    /Reboot ...
    /Info   Information commit/release verions on Github, host name, IP, memory usage, disk usage, cpu load.
    /Update Force update from Github to latest version of master branch.
    /Help   This menu"""


class Service:
    c_prefix = "- "
    c_info = "/Info"
    c_reboot = "/Reboot"
    c_update = "/Update"
    c_help = "/Help"

    def __init__(self, command: str = None, log_msg: str = None):
        self.__logger = LOGGER
        self.__log_msg = log_msg
        self.__command = command
        self.__help_txt = HELP_TEXT

        self.__menu_header = f"{NAME} functions:"

        self.__menu_dictionary = {
            0: self.c_reboot,
            1: self.c_info,
            2: self.c_update,
            3: self.c_help
        }

        self.__new_line = "\n"
        self.__empty = ""

    def execute_os_command(self):
        if self.__command is not None:
            try:
                self.__logger.info(
                    self.__log_msg) \
                    if self.__log_msg is not None else self.__command
                os.system(self.__command)
            except Exception as e:
                self.__logger.error(f"{e}")
        else:
            raise Exception("No executable command found!")

    def build_menu(self):
        try:
            m = f"{self.__menu_header}{self.__new_line}"
            self.__logger.debug(
                f"Build service menu: "
                f"{m.replace(self.__new_line, self.__empty)}")
            for key in self.__menu_dictionary.keys():
                line = f"{self.c_prefix}" \
                       f"{self.__menu_dictionary.get(key)}" \
                       f"{self.__new_line}"
                m += line
                self.__logger.debug(
                    f"Add line to menu: "
                    f"{line.replace(self.__new_line, self.__empty)}")
            return m
        except Exception as e:
            self.__logger.error(f"{e}")

    def build_help_text(self):
        return f"\n{self.__help_txt}"

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
    Service("shutdown -r now", log_msg).execute_os_command()


def system_info():
    s = Service()
    return s.system_info()


def get_help_text():
    s = Service()
    return s.build_help_text()


def service_menu():
    s = Service()
    return s.build_menu()


menu = service_menu()

if __name__ == '__main__':
    pass
