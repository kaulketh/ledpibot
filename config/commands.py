#!/usr/bin/python
# -*- coding: utf-8 -*-

from enum import unique, IntEnum


@unique
class Commands(IntEnum):
    start = 1
    stop = 2
    advent = 3
    animation = 4
    clock = 5
    xmas = 6
    cancel = 7

    def __int__(self):
        return self.value

    def __str__(self):
        return self.name
