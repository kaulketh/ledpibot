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


class OSCommand:
    logger = LOGGER

    c_prefix = "- "
    c_info = "/Info"
    c_reboot = "/Reboot"
    c_update = "/Update"
    c_test = "/TEST"

    __menu_header = f"{NAME} functions:"

    __menu_dictionary = {
        0: c_reboot,
        1: c_info,
        2: c_update,
        3: c_test
    }

    __new_line = "\n"
    __empty = ""

    def __init__(self, command: str = None, log_msg: str = None):
        self.__logger = OSCommand.logger
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
    def get_info_log(cls, n=None):
        lines = cls.__new_line
        n = 5 if n == None else n

        def logged(n, level='info'):
            this_folder = os.path.dirname(os.path.abspath(__file__))
            log_folder = os.path.join(this_folder, '../logs')
            file = f"{log_folder}/{level}.log"
            for line in get_last_n_lines(file, n):
                yield line

        for line in logged(n):
            lines += f"{line}{cls.__new_line}"

        return lines

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
    OSCommand("shutdown -r now", log_msg).execute()


def system_info():
    return OSCommand.system_info()


def get_last_n_lines(file_name, n):
    # Create an empty list to keep the track of last n lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location - 1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches n, then return the reversed list
                if len(list_of_lines) == n:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)

        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])

    # return the reversed list
    return list(reversed(list_of_lines))


menu = OSCommand.build_menu()

if __name__ == '__main__':
    pass
