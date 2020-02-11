#!/usr/bin/python3
# -*- coding: utf-8 -*-
# config/dictionary.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

import logger

log = logger.get_logger('Dictionary')
commands = []
txts = []
language = None

keys = {
    # messages
    0: {
        0: "wrong_id",
        1: "not_allowed",
        2: "pls_select",
        3: "called",
        4: "started",
        5: "cleared",
        6: "rebooted",
        7: "rotated"
    },

    # commands/buttons
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
        16: "strobe",
        17: "clock 3"
    }
}

translation = {
    "en": {
        "name": "English",
        keys[0].get(0): "`Hello {1}, this is a private bot!"
                        "\nID {0}, {2} {3} has been blocked."
                        "\nThanks for visit!`",
        keys[0].get(1): "* Not allowed for this bot\\! *",
        keys[0].get(2): " {0}, please make a suitable selection!",
        keys[0].get(3): "*{0}* called.",
        keys[0].get(4): "Bot ready for use.",
        keys[0].get(5): "Chat history cleared.",
        keys[0].get(6): "Device rebooted.",
        keys[0].get(7): "Logrotate executed manually.",

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
        "name": "Deustch",
        keys[0].get(0): "`Hallo {1}, dies ist ein privater Bot!"
                        "\nID {0}, {2} {3} wurde geblockt."
                        "\nDanke für den Besuch!`",
        keys[0].get(1): "* Nicht erlaubt für diesen Bot\\! *",
        keys[0].get(2): "{0}, bitte geeignete Auswahl treffen!",
        keys[0].get(3): "*{0}* aufgerufen.",
        keys[0].get(4): "Bot einsatzbereit.",
        keys[0].get(5): "Chatverlauf gelöscht.",
        keys[0].get(6): "Gerät neu gestartet.",
        keys[0].get(7): "Logrotate manuell ausgeführt.",

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


def _set_lng(lng: str):
    global language
    if lng not in translation:
        log.warning("Language \'{0}\' not found, set default language!".format(lng))
        language = "en"
    else:
        language = lng
    log.debug("Language set: {0}".format((translation[language].get('name')).upper()))


def _load_cmdtxts():
    global language
    for key in keys[1].keys():
        c = (translation[language].get(keys[1].get(key))).title()
        log.debug('Load command: ' + c)
        commands.append(c)


# def _load_msgtxts(index: int):
#     global language
#     m = translation[language].get(keys[0].get(index))
#     log.debug("Load message text fragment: {0}...".format(m[0:15]))
#     return m


def _load_msgtxts():
    global language
    for key in keys[0].keys():
        m = translation[language].get(keys[0].get(key))
        log.debug("Load message text fragment: {0}...".format(m[0:15]))
        txts.append(m)
    return txts


_set_lng("de")
_load_cmdtxts()
_load_msgtxts()
wrong_id, not_allowed, pls_select, called, started, cleared, rebooted, rotated = txts
