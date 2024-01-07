#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os
import yaml
from logger import LOGGER

# load settings, UI contents and secrets
FILES = "settings.yaml", "contents.yaml", "secrets.yaml"
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, FILES[0]), 'r', encoding='utf-8') as file:
    settings = yaml.safe_load(file)
with open(os.path.join(HERE, FILES[1]), 'r', encoding='utf-8') as file:
    translations = yaml.safe_load(file)
with open(os.path.join(HERE, FILES[2]), 'r', encoding='utf-8') as file:
    secrets = yaml.safe_load(file)

# secrets
ID_CHAT_THK = secrets.get("telegram").get("chat_ids").get("thk")
TOKEN_TELEGRAM_BOT = secrets.get("telegram").get("bot").get("token")

# define variables dynamically (settings first!)
# settings
for item in settings.items():
    _name = item[0]
    _value = item[1].get("value")
    _com = item[1].get("comment")
    globals()[_name] = _value
    LOGGER.debug(f"setting {_name} = {_value}")
# texts
commands = []
for item in translations.items():
    _type = item[1].get('type')
    _name = item[1].get('name')
    # noinspection PyUnresolvedReferences
    _value = item[1].get(language)
    _n = int(item[0])
    globals()[_name] = _value
    _value_hr = _value.replace("\n", "")  # human readable
    if _type == "btn_txt":
        # commands
        _n = len(commands)
        _value_hr = globals().get(_name).title()
        commands.append(_value_hr)
    LOGGER.debug(f"{_type}[{_n:02d}] {_name} = {_value_hr}")
