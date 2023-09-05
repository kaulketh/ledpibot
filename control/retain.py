#!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# retain.py
# created 05.09.2023
# Thomas Kaulke, kaulketh@gmail.com
# https://github.com/kaulketh
# -----------------------------------------------------------

import datetime
import os


class Retainer:
    """
    ... persists data in file.
    If file doesn't exist, will be created.
    """

    @classmethod
    def time_stamp(cls):
        d = datetime.datetime.now().date()
        t = datetime.datetime.now().time()
        return f"{d} {t} : "

    @classmethod
    def file_exists(cls, path):
        """
        File exists and is readable
        """
        return os.path.isfile(path) and os.access(path, os.R_OK)

    def __init__(self, file_path: str, ts_required=True):
        self.__path = file_path
        self.__ts = ts_required

    def __write(self, data, arg=None):
        with open(self.__path, arg) as f:
            f.write(str(data) if not isinstance(data, str) else data)

    def persist(self, data):
        if Retainer.file_exists(self.__path):
            if self.__ts:
                self.__write(f"\n{Retainer.time_stamp()}", arg="a")
            else:
                self.__write(f"\n", arg="a")
            self.__write(data, arg="a")

        else:
            if self.__ts:
                self.__write(Retainer.time_stamp(), arg="w")
                self.__write(data, arg="a")
            else:
                self.__write(data, arg="w")

    @property
    def ts(self):
        return self.__ts

    @ts.setter
    def ts(self, required):
        self.__ts = required

    @property
    def file(self):
        return self.__path

    @file.setter
    def file(self, f_path):
        self.__path = f_path

    @property
    def content(self):
        content = ""
        with open(self.__path, "r") as f:
            for line in f.readlines():
                content += line
        return content

    def get_line(self, line_number: int):
        i = line_number - 1
        with open(self.__path, "r") as f:
            line = f.readlines()[i]
        return line


if __name__ == '__main__':
    pass
