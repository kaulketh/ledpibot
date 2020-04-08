#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

import os
import subprocess

from logger import LOGGER

GIT_API_URL = "https://api.github.com/repos/kaulketh/ledpibot"
NAME = "Service"
HELP = """- After boot bot will inform user that it is ready to use via message
- Use in-app command /start to start
- Bot welcomes the user
- Select any function/color to run
- Bot messages about run and the clock time of auto-standby
- Keyboard changes to 2-button keyboard (stop/standby)
- User is able to stop the running function or to force standby
- Bot messages the clock time of restart
- When standby mode is reached only one stop button is displayed
    User is able to break the running standby
    It is possible to call in-app commands at any time!
    Call of an built-in command will break running function!
  
Functions/Animations:
    Clock 1: One LED per "pointer", Red hours "pointer", blue minutes "pointer", warm yellow running seconds "pointer" every 2.5 seconds
    Clock 2: One LED per "pointer", Red hours "pointer", blue minutes "pointer", a blue running light every 2.5 minutes from the current "minute" to the "12" 
    Clock 3: One LED per "pointer", Red hours "pointer", blue minutes "pointer", green seconds "scale" will extends every 2.5 seconds, there is also a "dial", a subtly warm yellow LED on each "number".
    Clock 4: Colorful, full color "scale" to minute, hour, second, "scales" will overridden and colors mixed/changed thus 
    Clock 5: Red hours "pointer", blue minutes "pointer" and a warm yellow 1 second "pendulum" over all LEDs
    Advent: Advent calendar, works in December only! For every day of December will one LED flickering like a candle light. If it is Advent Sunday it flickers red. If month is other than December all LEDs flickering in red as warning  
    Candles: Each LED flickers like candle light
    Rainbow: Rainbow animation with circular fading effect
    Theater: Extremely colorful animation with chaser, spinning, wiping effects
    Strobe: Emitting brief and rapid flashes of white light in random frequency
    Colors: Switching simple colors in random time periods
    Colors 2: Fading over simple colors in random time periods
    All LEDs at once can switched to: red, blue, green, white, yellow, orange, violet
    
Service menu: 
    /Reboot : ...
    /Info : Information about latest commit/release verions on Github, host name, IP, memory usage, disk usage, cpu load
    /Update : Force update from Github to the latest version in master branch
    /Help : This menu
"""


class Service:
    logger = LOGGER

    c_prefix = "- "
    c_info = "/Info"
    c_reboot = "/Reboot"
    c_update = "/Update"
    c_help = "/Help"

    __menu_header = f"{NAME} functions:"

    __menu_dictionary = {
        0: c_reboot,
        1: c_info,
        2: c_update,
        3: c_help
    }

    __new_line = "\n"
    __empty = ""

    def __init__(self, command: str = None, log_msg: str = None):
        self.__logger = Service.logger
        self.__log_msg = log_msg
        self.__command = command

    def execute(self):
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

    @classmethod
    def build_menu(cls):
        try:
            m = f"{cls.__menu_header}{cls.__new_line}"
            cls.logger.debug(
                f"Build service menu: "
                f"{m.replace(cls.__new_line, cls.__empty)}")
            for key in cls.__menu_dictionary.keys():
                line = f"{cls.c_prefix}" \
                       f"{cls.__menu_dictionary.get(key)}" \
                       f"{cls.__new_line}"
                m += line
                cls.logger.debug(
                    f"Add line to menu: "
                    f"{line.replace(cls.__new_line, cls.__empty)}")
            return m
        except Exception as e:
            cls.logger.error(f"{e}")

    @classmethod
    def help(cls):
        # with open('MANUAL.MD', 'r') as file:
        #     html = markdown.markdown(text=file.read())
        #     soup = BeautifulSoup(html, 'html.parser')
        #     out = ''.join(soup.findAll(text=True))
        # return (out[out.index('Main mode'):out.index('Logging')])
        return HELP

    @classmethod
    def system_info(cls):
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
                   f"{cls.__latest_release()} " \
                   f"({cls.__latest_commit()}){cls.__new_line}" \
                   f"{ip}{cls.__new_line}" \
                   f"{m}{cls.__new_line}" \
                   f"{d}{cls.__new_line}" \
                   f"{c}" \
                .replace("b'", "").replace("'", "").replace("\\n", "")
        except Exception as e:
            cls.logger.error(f"{e}")

    @classmethod
    def __latest_commit(cls):
        commit = f"curl -s {GIT_API_URL}/commits/master --insecure "
        latest_com = f"{subprocess.check_output(commit, shell=True)[12:46]}" \
                     f"".replace("b'", "").replace("'", "").replace("\\n", "")
        commit_url_text = f"[{latest_com[0:7]}]" \
                          f"(https://github.com/kaulketh/ledpibot/commit/" \
                          f"{latest_com})"
        return commit_url_text

    @classmethod
    def __latest_release(cls):
        release = f"curl -s {GIT_API_URL}/releases/latest --insecure |" \
                  " grep -Po '\"tag_name\": \"\\K.*?(?=\")'"
        return f"{subprocess.check_output(release, shell=True)}" \
            .replace("b'", "").replace("'", "").replace("\\n", "")


def reboot_device(log_msg: str = None):
    Service("shutdown -r now", log_msg).execute()


def system_info():
    return Service.system_info()



menu = Service.build_menu()

if __name__ == '__main__':
    pass
