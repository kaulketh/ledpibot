#!/usr/bin/python3
# -*- coding: utf-8 -*-
# config/dictionary.py
"""
Translations dictionary for command/button and message texts.
for emoji unicode refer https://unicode.org/emoji/charts/full-emoji-list.html
"""
__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

__maintainer___ = "Thomas Kaulke"
__status__ = "Development"

import logger
from .settings import STANDBY_MINUTES

log = logger.get_logger('Dictionary')
language = None
translations = None

keys = {
    0: {
        "name": "message text",
        0: "wrong_id",
        1: "not_allowed",
        2: "pls_select",
        3: "called",
        4: "started",
        5: "cleared",
        6: "rebooted",
        7: "rotated",
        8: "stopped",
        9: "standby",
        10: "stop_msg"
    },
    1: {
        "name": "command/button text",
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
        keys[0].get(2): " Please make a suitable selection, {0}!",
        keys[0].get(3): "*{0}* was started for a maximum of " + str(STANDBY_MINUTES) + " minutes\\.",
        keys[0].get(4): "Bot ready for use.",
        keys[0].get(5): "Chat history cleared.",
        keys[0].get(6): "Device rebooted.",
        keys[0].get(7): "Logrotate executed manually.",
        keys[0].get(8): "Bot stopped.",
        keys[0].get(9): "Stopped, automatic standby after " + str(STANDBY_MINUTES) + " minutes.\nPlease restart!",
        keys[0].get(10): "Everything stopped.",

        keys[1].get(0): "stop",
        keys[1].get(1): "start",
        keys[1].get(2): "advent",
        keys[1].get(3): "candles",
        keys[1].get(4): "clock 1",
        keys[1].get(5): "clock 2",
        keys[1].get(6): "rainbow",
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
        "name": "Deutsch",
        keys[0].get(0): "`Hallo {1}, dies ist ein privater Bot!"
                        "\nID {0}, {2} {3} wurde geblockt."
                        "\nDanke für den Besuch!`",
        keys[0].get(1): "* Nicht erlaubt für diesen Bot\\! *",
        keys[0].get(2): "Bitte triff eine Auswahl, {0}.",
        keys[0].get(3): "*{0}*  Animation läuft für maximal " + str(STANDBY_MINUTES) + " Minuten\\.",
        keys[0].get(4): "Bot ist einsatzbereit.",
        keys[0].get(5): "Chatverlauf wurde gelöscht.",
        keys[0].get(6): "Gerät wird neu gestartet.",
        keys[0].get(7): "Logrotate manuell ausgeführt.",
        keys[0].get(8): "Bot angehalten!",
        keys[0].get(9): "Gestoppt, automatischer Standby nach " + str(STANDBY_MINUTES) + " Minuten.\nBitte Neustart!",
        keys[0].get(10): "Alles gestoppt.",

        keys[1].get(0): u'\U000023F9',
        keys[1].get(1): u'\U000025B6',
        keys[1].get(2): u'\U0001F384',
        keys[1].get(3): u'\U0001F56F',
        keys[1].get(4): u'\U000023F0',
        keys[1].get(5): u'\U0001F55C',
        keys[1].get(6): u'\U0001F308',
        keys[1].get(7): u'\U0001F3AA',
        keys[1].get(8): u'\U0001F7E5',
        keys[1].get(9): u'\U0001F7E6',
        keys[1].get(10): u'\U0001F7E9',
        keys[1].get(11): u'\U0001F7E8',
        keys[1].get(12): u'\U0001F7E7',
        keys[1].get(13): u'\U00002B1C',
        keys[1].get(14): u'\U0001F7EA',
        keys[1].get(15): u'\U0001F500',
        keys[1].get(16): u'\U000026A1',
        keys[1].get(17): u'\U000023F1'
    }

}


def _set_language(lng='en'):
    """
    Set chat language, default = English.

    :param lng: language key (i.e. 'de')
    :return: None (set global chat language)
    """
    global language
    if lng not in translation:
        log.warning("Language key \'{0}\' not found, set default chat language!".format(lng))
        language = 'en'
    else:
        language = lng
    log.debug("Chat language: {0}".format((translation[language].get('name')).upper()))


def _get_translations(key_index):
    """
    Load translations from dictionary.

    :param key_index: 0 = messages, 1 = commands
    :return: list of texts
    """
    global language, translations
    translations = []

    # noinspection PyGlobalUndefined
    def generated_texts(i: int):
        global text
        for k in keys[i].keys():
            if isinstance(k, int):
                text = translation[language].get(keys[i].get(k))
                if i == 1:
                    text = text.title()
                log.debug("Load {0} ({1}:{2}) {3}".format(
                    str(keys[i].get("name")), str(k), str(keys[i].get(k)), text.replace("\n", " ")))
                yield text

    try:
        for t in generated_texts(key_index):
            translations.append(t)
        return translations
    except Exception as e:
        log.error('Error while import from translations! ' + str(e))


_set_language("de")
wrong_id, not_allowed, pls_select, called, started, cleared, rebooted, rotated, stopped, standby, stop_msg \
    = _get_translations(0)
commands = _get_translations(1)
