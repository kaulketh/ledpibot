#!/usr/bin/python3
# -*- coding: utf-8 -*-


__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"
__doc__ = "Translations dictionary for labels and message texts."

from logger import LOGGER

assignment = {}
language: str = ""

# text type constants
RUNNING = "Bot is running..."
CMD = "command"
MSG = "message"
DE = "de"
EN = "en"
FR = "fr"
NAME = "name"

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
        21: "clock 6",
        22: "clock 7",
        23: "rainbow 2",
        24: "theater 2",
        25: "standby"

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
        7: "Bot pausiert!",
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
        32: "uhr 6",
        33: "uhr 7",
        34: "regenbogn 2",
        35: "theater 2",
        36: "Bot-Update, Reboot folgt.",
        37: "Standby"

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
        7: "Bot paused.",
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
        32: "clock 6",
        33: "clock 7",
        34: "rainbow 2",
        35: "theater 2",
        36: "Bot update, reboot shortly.",
        37: "Standby"

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
        7: "Bot en pause!",
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
        32: "montre 6",
        33: "montre 7",
        34: "arc en ciel 2",
        35: "théâtre 2",
        36: "Mise à jour, le bot est redémarré.",
        37: "Etre prêt"

    }
}


def __assign_texts(lng_key: str):
    """
    Assignment of the texts to the messages/commands according to language

    :param lng_key: language key
    :return: None (setup global assignment of texts)
    """

    text_assignments = {}
    LOGGER.debug(
        f"Assign {languages[lng_key].get(NAME)} texts "
        f"to messages and commands.")

    # Messages
    for i in range(0, len(texts[MSG]) - 1):
        text_assignments[texts[MSG].get(i)] = texts[lng_key].get(i)
    # Commands
    for i in range(0, len(texts[CMD]) - 1):
        text_assignments[texts[CMD].get(i)] = \
            texts[lng_key].get(i + len(texts[MSG]) - 1)
    # Message 'Update'
    text_assignments[texts[MSG].get(11)] = texts[lng_key].get(36)
    # Command 'Standby'
    text_assignments[texts[CMD].get(25)] = texts[lng_key].get(37)

    languages[lng_key].update(text_assignments)

    global assignment
    assignment = languages
    LOGGER.debug(f"{languages[lng_key].get(NAME)} text library built.")


def build_text_libraries():
    LOGGER.debug("Initialize text libraries of possible languages.")
    for k in languages.keys():
        __assign_texts(k)


def set_language(lng=EN):
    """
    Set chat language, default = English.

    :param lng: language key (i.e. 'de')
    :return: None (set up global chat language)
    """

    if lng not in assignment:
        global language
        LOGGER.warning(
            f"Language key \'{lng}\' not found, set default chat language!")
        language = EN
    else:
        language = lng
    LOGGER.info(
        f"Chat language was set to '{(assignment[language].get(NAME))}'.")


def get_texts(text_type):
    """
    Get text translations.

    :param text_type: messages, commands
    :return: list of texts
    """
    global language, assignment
    translations = []

    def text_generator(_type: str):
        for key in texts[_type].keys():
            txt = assignment[language].get(
                texts[_type].get(key)).title() if _type == CMD \
                else assignment[language].get(texts[_type].get(key))
            newline, space = ("\n", " ")
            LOGGER.debug(
                f"{key}: {texts[_type].get(key)} = "
                f"{txt.replace(newline, space)}"

            )
            yield txt

    try:
        for t in text_generator(text_type):
            translations.append(t)
        return translations
    except Exception as e:
        LOGGER.error(f"Error while import from translations: {e}")


if __name__ == '__main__':
    pass
