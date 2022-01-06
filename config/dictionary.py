#!/usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "Translations dictionary for labels and message texts."

from logger import LOGGER

RUNNING = "Bot is running..."

CMD = "command"
MSG = "message"
DE = "de"
EN = "en"
FR = "fr"
NAME = "name"

assignment = {}
language: str = ""

languages = {
    DE: {NAME: "German"},
    EN: {NAME: "English"},
    FR: {NAME: "French"},
}

# noinspection SpellCheckingInspection
texts = {
    MSG: {
        0: "m_wrong_id",
        1: "m_not_allowed",
        2: "m_pls_select",
        3: "m_called",
        4: "m_started",
        5: "m_rebooted",
        6: "m_rotated",
        7: "m_stopped",
        8: "m_standby",
        9: "m_stop_f",
        10: "m_killed",
        11: "m_updated"
    },
    CMD: {
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
        20: "demo 2",
        21: "standby"
    },
    DE: {
        0: "`Hallo {1}, dies ist ein privater Bot!"
           "\nID {0}, {2} {3} wurde geblockt.\nDanke für den Besuch!`",
        1: "* Nicht erlaubt für diesen Bot\\! *",
        2: "Bitte triff eine Auswahl, {0}.",
        3: "*{0}* läuft bis {1}",
        4: "Bot ist einsatzbereit.",
        5: "Gerät wird neu gestartet.",
        6: "Logrotate manuell ausgeführt.",
        7: "Bot angehalten!",
        8: "Standby: {0}\nNeustart um {1}",
        9: "{0} gestoppt.",
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

        32: "Bot-Update, Reboot folgt.",

        33: "Standby"
    },

    EN: {
        0: "`Hello {1}, this is a private bot!"
           "\nID {0}, {2} {3} has been blocked.\nThanks for visit!`",
        1: "* Not allowed for this bot\\! *",
        2: "Please make a suitable selection, {0}!",
        3: "*{0}* runs until {1}",
        4: "Bot ready for use.",
        5: "Device rebooted.",
        6: "Logrotate executed manually.",
        7: "Bot stopped.",
        8: "Standby: {0}\nRestart at {1}",
        9: "{0} stopped.",
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

        32: "Bot update, reboot shortly.",

        33: "Standby"
    },
    FR: {
        0: "`Bonjour {1}, c'est un bot privé!"
           "\nL'Id {0}, {2} {3} a été bloqué.\nMerci de votre visite!`",
        1: "* Non autorisé pour ce bot\\! *",
        2: "Veuillez faire une sélection, {0}.",
        3: "*{0}* s'exécute jusqu'à {1}",
        4: "Le bot est prêt à l'emploi.",
        5: "L'appareil est redémarré.",
        6: "Logrotate exécuté manuellement.",
        7: "Bot arrêté!",
        8: "Veille: {0}\nRedémarrez à {1}",
        9: "{0} arrêté.",
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

        32: "Mise à jour, le bot est redémarré.",

        33: "Etre prêt"
    }
}


def assign_texts(lang: str):
    """
    Assignment of the texts to the messages/commands according to the language

    :param lang: language key
    :return: None
    """

    text_assignments = {}
    for i in range(0, 11):
        text_assignments[texts[MSG].get(i)] = texts[lang].get(i)
    text_assignments[texts[MSG].get(11)] = texts[lang].get(32)
    for i in range(0, 21):
        text_assignments[texts[CMD].get(i)] = texts[lang].get(i + 11)
    text_assignments[texts[CMD].get(21)] = texts[lang].get(33)
    languages[lang].update(text_assignments)

    global assignment
    assignment = languages


def set_language(lng=EN):
    """
    Set chat language, default = English.

    :param lng: language key (i.e. 'de')
    :return: None (set global chat language)
    """

    if lng not in assignment:
        global language
        LOGGER.warning(
            f"Language key \'{lng}\' not found, set default chat language!")
        language = EN
    else:
        language = lng
    LOGGER.info(
        f"Apart from service menu chat language was set to '"
        f"{(assignment[language].get(NAME))}'.")


def get_translations(text_index):
    """
    Load translations from dictionary.

    :param text_index: messages, commands
    :return: list of texts
    """
    global language, assignment
    translations = []

    def generated_texts(key_type: str):
        for key in texts[key_type].keys():
            txt = assignment[language].get(
                texts[key_type].get(key)).title() if key_type == CMD \
                else assignment[language].get(texts[key_type].get(key))
            newline, space = ("\n", " ")
            LOGGER.debug(
                f"Load {key_type} ({key}:{texts[key_type].get(key)}) "
                f"{txt.replace(newline, space)}"
            )
            yield txt

    try:
        for t in generated_texts(text_index):
            translations.append(t)
        return translations
    except Exception as e:
        LOGGER.error(f"Error while import from translations: {e}")


def build_dictionary():
    LOGGER.debug("Build dictionary of required strings...")
    for k in languages.keys():
        LOGGER.debug(f"Update {languages[k].get(NAME)} texts.")
        assign_texts(k)


if __name__ == '__main__':
    pass
