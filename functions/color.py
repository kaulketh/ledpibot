#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from rpi_ws281x import Color


def _get_color(r, g, b, bir=1):
    # bir => brightness/intense reducer
    c = Color(r // bir, g // bir, b // bir)
    return c


class OwnColors:
    class _AttribDict(dict):
        __slots__ = ()
        __getattr__ = dict.__getitem__
        __setattr__ = dict.__setitem__

    color = _AttribDict({
        "BLUE": _get_color(0, 0, 200),
        "GREEN": _get_color(0, 200, 0),
        "OFF": _get_color(0, 0, 0),
        "RED": _get_color(200, 0, 0),
        "WHITE": _get_color(255, 255, 255),
        "YELLOW": _get_color(92, 67, 6),
        "blue": _get_color(0, 50, 135, 3),
        "green": _get_color(0, 135, 50, 3),
        "less_intense_blue": _get_color(0, 0, 40),
        "less_intense_green": _get_color(6, 30, 10),
        "less_intense_red": _get_color(50, 0, 0),
        "less_intense_yellow": _get_color(92 // 4, 67 // 4, 6 // 4),
        "orange": _get_color(210, 70, 0, 3),
        "red": _get_color(165, 10, 10, 3),
        "violet": _get_color(238, 18, 137, 3),
        "white": _get_color(255, 255, 255, 6),
        "yellow": _get_color(255, 165, 0, 3)
    })


if __name__ == "__main__":
    pass
