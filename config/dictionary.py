#!/usr/bin/python3
# -*- coding: utf-8 -*-
# config/dictionary.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

# dictionary keys
lng = 'de'  # default chat language 'en' or 'de'

keys = {
    # message texts
    0: {
        0: "wrong_id",
        1: "not_allowed",
        2: "pls_select",
        3: "called"
    },

    # command/button texts
    1: {
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
}

# text translations
translation = {
    "en": {
        keys[0].get(0): "`Hello {1}, this is a private bot!"
                        "\nID {0}, {2} {3} has been blocked."
                        "\nThanks for visit!`",
        keys[0].get(1): "* Not allowed for this bot\\! "
                        "\nTry /start*",
        keys[0].get(2): " {0}, please make a suitable selection!",
        keys[0].get(3): "*{0}* called.",

        keys[1].get(0): "stop",
        keys[1].get(1): "start",
        keys[1].get(2): "advent",
        keys[1].get(3): "candles",
        keys[1].get(4): "clock 1",
        keys[1].get(5): "clock 2",
        keys[1].get(6): "multi",
        keys[1].get(7): "theater",
        keys[1].get(8): "red",
        keys[1].get(9): "blue",
        keys[1].get(10): "green",
        keys[1].get(11): "yellow",
        keys[1].get(12): "orange",
        keys[1].get(13): "white",
        keys[1].get(14): "pink",
        keys[1].get(15): "colors",
        keys[1].get(16): "strobe",
        keys[1].get(17): "clock 3"
    },

    "de": {
        keys[0].get(0): "`Hallo {1}, dies ist ein privater Bot!"
                        "\nID {0}, {2} {3} wurde geblockt."
                        "\nDanke für den Besuch!`",
        keys[0].get(1): "* Nicht erlaubt für diesen Bot\\!"
                        "\nVersuch /start *",
        keys[0].get(2): "{0}, bitte geeignete Auswahl treffen!",
        keys[0].get(3): "*{0}* aufgerufen.",

        keys[1].get(0): "stop",
        keys[1].get(1): "start",
        keys[1].get(2): "advent",
        keys[1].get(3): "kerzen",
        keys[1].get(4): "uhr 1",
        keys[1].get(5): "uhr 2",
        keys[1].get(6): "multi",
        keys[1].get(7): "theater",
        keys[1].get(8): "rot",
        keys[1].get(9): "blau",
        keys[1].get(10): "grün",
        keys[1].get(11): "gelb",
        keys[1].get(12): "orange",
        keys[1].get(13): "weiß",
        keys[1].get(14): "pink",
        keys[1].get(15): "farben",
        keys[1].get(16): "strobe",
        keys[1].get(17): "uhr 3"
    }

}

# text list of commands
commands = []
for key in keys[1].keys():
    commands.append((translation[lng].get(keys[1].get(key))).title())

# texts for messages
wrong_id = translation[lng].get(keys[0].get(0))
not_allowed = translation[lng].get(keys[0].get(1))
pls_select = translation[lng].get(keys[0].get(2))
called = translation[lng].get(keys[0].get(3))
