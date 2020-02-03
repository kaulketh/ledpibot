#!/usr/bin/python3
# -*- coding: utf-8 -*-
# config/dictionary.py
"""
author: Thomas Kaulke, kaulketh@gmail.com
"""

# set default chat language here
language = 'de'

dic = {
    "en": {"wrong_id": "`Hello {1}, this is a private bot!\nID {0}, {2} {3} has been blocked.\nThanks for visit!`",
           "not_allowed": "* Not allowed for this bot\\! \nTry /start*",
           "pls_select": " {0}, please make a suitable selection!",
           "called": "* called.",
           "stop": "stop",  # 0
           "start": "start",  # 1
           "advent": "advent",  # 2
           "candles": "candles",  # 3
           "clock 1": "clock 1",  # 4
           "clock 2": "clock 2",  # 5
           "rainbow": "rainbow",  # 6
           "theater": "theater",  # 7
           "red": "red",  # 8
           "blue": "blue",  # 9
           "green": "green",  # 10
           "yellow": "yellow",  # 11
           "orange": "orange",  # 12
           "white": "white",  # 13

           },
    "de": {
        "wrong_id": "`Hallo {1}, dies ist ein privater Bot!\nID {0}, {2} {3} wurde geblockt.\nDanke für den Besuch!`",
        "not_allowed": "* Nicht erlaubt für diesen Bot\\! \nVersuch /start *",
        "pls_select": "{0}, bitte geeignete Auswahl treffen!",
        "called": "* aufgerufen.",
        "stop": "stop",  # 0
        "start": "start",  # 1
        "advent": "advent",  # 2
        "candles": "kerzen",  # 3
        "clock 1": "uhr 1",  # 4
        "clock 2": "uhr 2",  # 5
        "rainbow": "regenbogen",  # 6
        "theater": "theater",  # 7
        "red": "rot",  # 8
        "blue": "blau",  # 9
        "green": "grün",  # 10
        "yellow": "gelb",  # 11
        "orange": "orange",  # 12
        "white": "weiß",  # 13

        }

}

commands = [dic[language].get("stop"),  # 0
            dic[language].get("start"),  # 1
            dic[language].get("advent"),  # 2
            dic[language].get("candles"),  # 3
            dic[language].get("clock 1"),  # 4
            dic[language].get("clock 2"),  # 5
            dic[language].get("rainbow"),  # 6
            dic[language].get("theater"),  # 7
            dic[language].get("red"),  # 8
            dic[language].get("blue"),  # 9
            dic[language].get("green"),  # 10
            dic[language].get("yellow"),  # 11
            dic[language].get("orange"),  # 12
            dic[language].get("white"),  # 13
            ]

wrong_id = dic[language].get("wrong_id")
not_allowed = dic[language].get("not_allowed")
pls_select = dic[language].get("pls_select")
called = dic[language].get("called")
