#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Translations dictionary for command/button label and message texts.
for emoji unicode refer https://unicode.org/emoji/charts/full-emoji-list.html
"""

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

from logger import LOGGER
from .settings import COUNTDOWN_MINUTES, COUNTDOWN_RESTART_MINUTES

# noinspection SpellCheckingInspection
txts = {
    "message": {
        0: "wrong_id",
        1: "not_allowed",
        2: "pls_select",
        3: "called",
        4: "started",
        5: "rebooted",
        6: "rotated",
        7: "stopped",
        8: "standby",
        9: "stop_msg",
        10: "killed",
        11: "updated"
    },
    "command": {
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
        14: "violet",
        15: "demo",
        16: "strobe",
        17: "clock 3",
        18: "clock 4",
        19: "clock 5",
        20: "demo 2"
    },
    "de": {
        0: "`Hallo {1}, dies ist ein privater Bot!\nID {0}, {2} {3} wurde geblockt.\nDanke für den Besuch!`",
        1: "* Nicht erlaubt für diesen Bot\\! *",
        2: "Bitte triff eine Auswahl, {0}.",
        3: "*{0}* läuft für " + str(COUNTDOWN_MINUTES // 60) + " Stunden",
        4: "Bot ist einsatzbereit.",
        5: "Gerät wird neu gestartet.",
        6: "Logrotate manuell ausgeführt.",
        7: "Bot angehalten!",
        8: f"Gestoppt, automatischer Standby nach {COUNTDOWN_MINUTES // 60} Stunden."
           f"\nNeustart in {COUNTDOWN_RESTART_MINUTES // 60} Stunden!",
        9: "Alles gestoppt.",
        10: "Kompletten Bot-Prozess abgebrochen!",
        11: "stop",
        12: "start",
        13: "advent",
        14: "kerzen",
        15: "uhr 1",
        16: "uhr 2",
        17: "regenbogen",
        18: "theater",
        19: "rot",
        20: "blau",
        21: "grün",
        22: "gelb",
        23: "orange",
        24: "weiß",
        25: "violett",
        26: "farben",
        27: "strobe",
        28: "uhr 3",
        29: "uhr 4",
        30: "uhr 5",
        31: "farben 2",
        32: "Bot-Update, Reboot folgt."
    },
    "emoji": {
        0: u'\U000023F9',
        1: u'\U000025B6',
        2: u'\U0001F384',
        3: u'\U0001F56F',
        4: u'\U000023F0',
        5: u'\U0001F55C',
        6: u'\U0001F308',
        7: u'\U0001F3AA',
        8: u'\U0001F7E5',
        9: u'\U0001F7E6',
        10: u'\U0001F7E9',
        11: u'\U0001F7E8',
        12: u'\U0001F7E7',
        13: u'\U00002B1C',
        14: u'\U0001F7EA',
        15: u'\U0001F500',
        16: u'\U000026A1',
        17: u'\U000023F1',
        18: u'\U000023F2',
        19: u'\U0001F570',
        20: u'\U0001F501'
    },
    "en": {
        0: "`Hello {1}, this is a private bot!\nID {0}, {2} {3} has been blocked.\nThanks for visit!`",
        1: "* Not allowed for this bot\\! *",
        2: "Please make a suitable selection, {0}!",
        3: "*{0}* was started for " + str(COUNTDOWN_MINUTES // 60) + " hours",
        4: "Bot ready for use.",
        5: "Device rebooted.",
        6: "Logrotate executed manually.",
        7: "Bot stopped.",
        8: f"Stopped, automatic standby after {COUNTDOWN_MINUTES // 60} hours."
           f"\nRestart in {COUNTDOWN_RESTART_MINUTES // 60} hours!",
        9: "Everything stopped.",
        10: "Bot process killed!",
        11: "stop",
        12: "start",
        13: "advent",
        14: "candles",
        15: "clock 1",
        16: "clock 2",
        17: "rainbow",
        18: "theater",
        19: "red",
        20: "blue",
        21: "green",
        22: "yellow",
        23: "orange",
        24: "white",
        25: "violet",
        26: "colors",
        27: "strobe",
        28: "clock 3",
        29: "clock 4",
        30: "clock 5",
        31: "colors 2",
        32: "Bot update, reboot shortly."
    },
    "fr": {
        0: "`Bonjour {1}, c'est un bot privé!\nL'Id {0}, {2} {3} a été bloqué.\nMerci de votre visite!`",
        1: "* Non autorisé pour ce bot\\! *",
        2: "Veuillez faire une sélection, {0}.",
        3: "*{0}* dure " + str(COUNTDOWN_MINUTES // 60) + " heures",
        4: "Le bot est prêt à l'emploi.",
        5: "L'appareil est redémarré.",
        6: "Logrotate exécuté manuellement.",
        7: "Bot arrêté!",
        8: f"Arrêt, mise en veille automatique après {COUNTDOWN_MINUTES // 60} heures."
           f"\nRedémarrez en {COUNTDOWN_RESTART_MINUTES // 60} heures!",
        9: "Tout s'est arrêté!",
        10: "Processus de bot complet annulé!",
        11: "stop",
        12: "start",
        13: "advent",
        14: "chandelles",
        15: "montre 1",
        16: "montre 2",
        17: "arc en ciel",
        18: "théâtre",
        19: "rouge",
        20: "bleu",
        21: "vert",
        22: "jaune",
        23: "orange",
        24: "blanc",
        25: "violet",
        26: "couleurs",
        27: "strobe",
        28: "montre 3",
        29: "montre 4",
        30: "montre 5",
        31: "couleurs 2",
        32: "Mise à jour, le bot est redémarré."
    }
}

translation = {
    "de": {
        "name": "German",
        txts["message"].get(0): txts["de"].get(0),
        txts["message"].get(1): txts["de"].get(1),
        txts["message"].get(2): txts["de"].get(2),
        txts["message"].get(3): txts["de"].get(3),
        txts["message"].get(4): txts["de"].get(4),
        txts["message"].get(5): txts["de"].get(5),
        txts["message"].get(6): txts["de"].get(6),
        txts["message"].get(7): txts["de"].get(7),
        txts["message"].get(8): txts["de"].get(8),
        txts["message"].get(9): txts["de"].get(9),
        txts["message"].get(10): txts["de"].get(10),
        txts["command"].get(0): txts["de"].get(11),
        txts["command"].get(1): txts["de"].get(12),
        txts["command"].get(2): txts["de"].get(13),
        txts["command"].get(3): txts["de"].get(14),
        txts["command"].get(4): txts["de"].get(15),
        txts["command"].get(5): txts["de"].get(16),
        txts["command"].get(6): txts["de"].get(17),
        txts["command"].get(7): txts["de"].get(18),
        txts["command"].get(8): txts["de"].get(19),
        txts["command"].get(9): txts["de"].get(20),
        txts["command"].get(10): txts["de"].get(21),
        txts["command"].get(11): txts["de"].get(22),
        txts["command"].get(12): txts["de"].get(23),
        txts["command"].get(13): txts["de"].get(24),
        txts["command"].get(14): txts["de"].get(25),
        txts["command"].get(15): txts["de"].get(26),
        txts["command"].get(16): txts["de"].get(27),
        txts["command"].get(17): txts["de"].get(28),
        txts["command"].get(18): txts["de"].get(29),
        txts["command"].get(19): txts["de"].get(30),
        txts["command"].get(20): txts["de"].get(31),
        txts["message"].get(11): txts["de"].get(32)

    },
    "de_emoji": {
        "name": "German with emoji",
        txts["message"].get(0): txts["de"].get(0),
        txts["message"].get(1): txts["de"].get(1),
        txts["message"].get(2): txts["de"].get(2),
        txts["message"].get(3): txts["de"].get(3),
        txts["message"].get(4): txts["de"].get(4),
        txts["message"].get(5): txts["de"].get(5),
        txts["message"].get(6): txts["de"].get(6),
        txts["message"].get(7): txts["de"].get(7),
        txts["message"].get(8): txts["de"].get(8),
        txts["message"].get(9): txts["de"].get(9),
        txts["message"].get(10): txts["de"].get(10),
        txts["command"].get(0): txts["emoji"].get(0),
        txts["command"].get(1): txts["emoji"].get(1),
        txts["command"].get(2): txts["emoji"].get(2),
        txts["command"].get(3): txts["emoji"].get(3),
        txts["command"].get(4): txts["emoji"].get(4),
        txts["command"].get(5): txts["emoji"].get(5),
        txts["command"].get(6): txts["emoji"].get(6),
        txts["command"].get(7): txts["emoji"].get(7),
        txts["command"].get(8): txts["emoji"].get(8),
        txts["command"].get(9): txts["emoji"].get(9),
        txts["command"].get(10): txts["emoji"].get(10),
        txts["command"].get(11): txts["emoji"].get(11),
        txts["command"].get(12): txts["emoji"].get(12),
        txts["command"].get(13): txts["emoji"].get(13),
        txts["command"].get(14): txts["emoji"].get(14),
        txts["command"].get(15): txts["emoji"].get(15),
        txts["command"].get(16): txts["emoji"].get(16),
        txts["command"].get(17): txts["emoji"].get(17),
        txts["command"].get(18): txts["emoji"].get(18),
        txts["command"].get(19): txts["emoji"].get(19),
        txts["command"].get(20): txts["emoji"].get(20),
        txts["message"].get(11): txts["de"].get(32)
    },
    "en": {
        "name": "English",
        txts["message"].get(0): txts["en"].get(0),
        txts["message"].get(1): txts["en"].get(1),
        txts["message"].get(2): txts["en"].get(2),
        txts["message"].get(3): txts["en"].get(3),
        txts["message"].get(4): txts["en"].get(4),
        txts["message"].get(5): txts["en"].get(5),
        txts["message"].get(6): txts["en"].get(6),
        txts["message"].get(7): txts["en"].get(7),
        txts["message"].get(8): txts["en"].get(8),
        txts["message"].get(9): txts["en"].get(9),
        txts["message"].get(10): txts["en"].get(10),
        txts["command"].get(0): txts["en"].get(11),
        txts["command"].get(1): txts["en"].get(12),
        txts["command"].get(2): txts["en"].get(13),
        txts["command"].get(3): txts["en"].get(14),
        txts["command"].get(4): txts["en"].get(15),
        txts["command"].get(5): txts["en"].get(16),
        txts["command"].get(6): txts["en"].get(17),
        txts["command"].get(7): txts["en"].get(18),
        txts["command"].get(8): txts["en"].get(19),
        txts["command"].get(9): txts["en"].get(20),
        txts["command"].get(10): txts["en"].get(21),
        txts["command"].get(11): txts["en"].get(22),
        txts["command"].get(12): txts["en"].get(23),
        txts["command"].get(13): txts["en"].get(24),
        txts["command"].get(14): txts["en"].get(25),
        txts["command"].get(15): txts["en"].get(26),
        txts["command"].get(16): txts["en"].get(27),
        txts["command"].get(17): txts["en"].get(28),
        txts["command"].get(18): txts["en"].get(29),
        txts["command"].get(19): txts["en"].get(30),
        txts["command"].get(20): txts["en"].get(31),
        txts["message"].get(11): txts["en"].get(32)
    },
    "en_emoji": {
        "name": "English with emoji",
        txts["message"].get(0): txts["en"].get(0),
        txts["message"].get(1): txts["en"].get(1),
        txts["message"].get(2): txts["en"].get(2),
        txts["message"].get(3): txts["en"].get(3),
        txts["message"].get(4): txts["en"].get(4),
        txts["message"].get(5): txts["en"].get(5),
        txts["message"].get(6): txts["en"].get(6),
        txts["message"].get(7): txts["en"].get(7),
        txts["message"].get(8): txts["en"].get(8),
        txts["message"].get(9): txts["en"].get(9),
        txts["message"].get(10): txts["en"].get(10),
        txts["command"].get(0): txts["emoji"].get(0),
        txts["command"].get(1): txts["emoji"].get(1),
        txts["command"].get(2): txts["emoji"].get(2),
        txts["command"].get(3): txts["emoji"].get(3),
        txts["command"].get(4): txts["emoji"].get(4),
        txts["command"].get(5): txts["emoji"].get(5),
        txts["command"].get(6): txts["emoji"].get(6),
        txts["command"].get(7): txts["emoji"].get(7),
        txts["command"].get(8): txts["emoji"].get(8),
        txts["command"].get(9): txts["emoji"].get(9),
        txts["command"].get(10): txts["emoji"].get(10),
        txts["command"].get(11): txts["emoji"].get(11),
        txts["command"].get(12): txts["emoji"].get(12),
        txts["command"].get(13): txts["emoji"].get(13),
        txts["command"].get(14): txts["emoji"].get(14),
        txts["command"].get(15): txts["emoji"].get(15),
        txts["command"].get(16): txts["emoji"].get(16),
        txts["command"].get(17): txts["emoji"].get(17),
        txts["command"].get(18): txts["emoji"].get(18),
        txts["command"].get(19): txts["emoji"].get(19),
        txts["command"].get(20): txts["emoji"].get(20),
        txts["message"].get(11): txts["en"].get(32)
    },
    "fr": {
        "name": "French",
        txts["message"].get(0): txts["fr"].get(0),
        txts["message"].get(1): txts["fr"].get(1),
        txts["message"].get(2): txts["fr"].get(2),
        txts["message"].get(3): txts["fr"].get(3),
        txts["message"].get(4): txts["fr"].get(4),
        txts["message"].get(5): txts["fr"].get(5),
        txts["message"].get(6): txts["fr"].get(6),
        txts["message"].get(7): txts["fr"].get(7),
        txts["message"].get(8): txts["fr"].get(8),
        txts["message"].get(9): txts["fr"].get(9),
        txts["message"].get(10): txts["fr"].get(10),
        txts["command"].get(0): txts["fr"].get(11),
        txts["command"].get(1): txts["fr"].get(12),
        txts["command"].get(2): txts["fr"].get(13),
        txts["command"].get(3): txts["fr"].get(14),
        txts["command"].get(4): txts["fr"].get(15),
        txts["command"].get(5): txts["fr"].get(16),
        txts["command"].get(6): txts["fr"].get(17),
        txts["command"].get(7): txts["fr"].get(18),
        txts["command"].get(8): txts["fr"].get(19),
        txts["command"].get(9): txts["fr"].get(20),
        txts["command"].get(10): txts["fr"].get(21),
        txts["command"].get(11): txts["fr"].get(22),
        txts["command"].get(12): txts["fr"].get(23),
        txts["command"].get(13): txts["fr"].get(24),
        txts["command"].get(14): txts["fr"].get(25),
        txts["command"].get(15): txts["fr"].get(26),
        txts["command"].get(16): txts["fr"].get(27),
        txts["command"].get(17): txts["fr"].get(28),
        txts["command"].get(18): txts["fr"].get(29),
        txts["command"].get(19): txts["fr"].get(30),
        txts["command"].get(20): txts["fr"].get(31),
        txts["message"].get(11): txts["fr"].get(32)
    }
}


# noinspection PyGlobalUndefined
def set_language(lng='en'):
    """
    Set chat language, default = English.

    :param lng: language key (i.e. 'de')
    :return: None (set global chat language)
    """
    global language
    if lng not in translation:
        LOGGER.warning(f"Language key \'{lng}\' not found, set default chat language!")
        language = 'en'
    else:
        language = lng
    LOGGER.info(f"Apart from service menu chat language is set to '{(translation[language].get('name'))}'.")


# noinspection PyGlobalUndefined
def get_translations(text_index):
    """
    Load translations from dictionary.

    :param text_index: messages, commands
    :return: list of texts
    """
    global language, translations, text
    translations = []
    text = ""

    # noinspection PyShadowingNames
    def generated_texts(txt: str):
        for k in txts[txt].keys():
            text = translation[language].get(txts[txt].get(k)).title() if txt == "command" \
                else translation[language].get(txts[txt].get(k))
            newline, space = ("\n", " ")
            LOGGER.debug(f"Load {txt} ({k}:{txts[txt].get(k)}) {text.replace(newline, space)}")
            yield text

    try:
        for t in generated_texts(text_index):
            translations.append(t)
        return translations
    except Exception as e:
        LOGGER.error(f"Error while import from translations: {e}")


if __name__ == '__main__':
    pass
