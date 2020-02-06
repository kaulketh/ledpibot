#!/usr/bin/python3
# -*- coding: utf-8 -*-
# config/dictionary.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

# default chat language
# lng = 'en'
lng = 'de'

# keys of message texts
t_ks = {
    0: "wrong_id",
    1: "not_allowed",
    2: "pls_select",
    3: "called"
}

# keys of command texts
c_ks = {
    0: "stop",
    1: "start",
    2: "advent",
    3: "candles",
    4: "clock 1",
    5: "clock 2",
    6: "rainbow",
    7: "theater",
    8: "red",
    9: "blue",
    10: "green",
    11: "yellow",
    12: "orange",
    13: "white",
    14: "pink",
    15: "demo",
    16: "strob",
    17: "clock 3"
}

# text translations
trnslt = {
    "en": {
        t_ks.get(0): "`Hello {1}, this is a private bot!\nID {0}, {2} {3} has been blocked.\nThanks for visit!`",
        t_ks.get(1): "* Not allowed for this bot\\! \nTry /start*",
        t_ks.get(2): " {0}, please make a suitable selection!",
        t_ks.get(3): "* called.",
        c_ks.get(0): "stop",
        c_ks.get(1): "start",
        c_ks.get(2): "advent",
        c_ks.get(3): "candles",
        c_ks.get(4): "clock 1",
        c_ks.get(5): "clock 2",
        c_ks.get(6): "rainbow",
        c_ks.get(7): "theater",
        c_ks.get(8): "red",
        c_ks.get(9): "blue",
        c_ks.get(10): "green",
        c_ks.get(11): "yellow",
        c_ks.get(12): "orange",
        c_ks.get(13): "white",
        c_ks.get(14): "pink",
        c_ks.get(15): "colors",
        c_ks.get(16): "stroboscope",
        c_ks.get(17): "clock 3"
    },

    "de": {
        t_ks.get(0):
            "`Hallo {1}, dies ist ein privater Bot!\nID {0}, {2} {3} wurde geblockt.\nDanke für den Besuch!`",
        t_ks.get(1): "* Nicht erlaubt für diesen Bot\\! \nVersuch /start *",
        t_ks.get(2): "{0}, bitte geeignete Auswahl treffen!",
        t_ks.get(3): "* aufgerufen.",
        c_ks.get(0): "stop",
        c_ks.get(1): "start",
        c_ks.get(2): "advent",
        c_ks.get(3): "kerzen",
        c_ks.get(4): "uhr 1",
        c_ks.get(5): "uhr 2",
        c_ks.get(6): "regenbogen",
        c_ks.get(7): "theater",
        c_ks.get(8): "rot",
        c_ks.get(9): "blau",
        c_ks.get(10): "grün",
        c_ks.get(11): "gelb",
        c_ks.get(12): "orange",
        c_ks.get(13): "weiß",
        c_ks.get(14): "pink",
        c_ks.get(15): "farben",
        c_ks.get(16): "stroboskope",
        c_ks.get(17): "uhr 3"
    }

}

# text list of commands
commands = []
for key in c_ks:
    commands.append(trnslt[lng].get(c_ks.get(key)))

# texts for messages
wrong_id = trnslt[lng].get(t_ks.get(0))
not_allowed = trnslt[lng].get(t_ks.get(1))
pls_select = trnslt[lng].get(t_ks.get(2))
called = trnslt[lng].get(t_ks.get(3))
