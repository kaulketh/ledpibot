#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os

import yaml

from logger import LOGGER


class _AttribDict(dict):
    __slots__ = ()
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


# load settings, UI contents and secrets
CFG_FILES = _AttribDict({"settings": "settings.yaml",
                         "contents": "contents.yaml",
                         "secrets": "secrets.yaml"})
here = os.path.dirname(os.path.abspath(__file__))
data_read_in = []

# read files
for key in CFG_FILES.keys():
    with open(os.path.join(here, CFG_FILES.get(key)), 'r',
              encoding='utf-8') as file:
        data_read_in.append(yaml.safe_load(file))
        LOGGER.debug(f"{CFG_FILES.get(key)} read in")

# define variables dynamically (settings first!)
# settings
for item in data_read_in[0].items():
    _name = item[0]
    _value = item[1].get("value")
    _com = item[1].get("comment")
    globals()[_name] = _value
    LOGGER.debug(f"setting {_name} = {_value}")
# texts
commands = []
for item in data_read_in[1].items():
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

# secrets
ID_CHAT_THK = data_read_in[2].get("telegram").get("chat_ids").get("thk")
TOKEN_TELEGRAM_BOT = data_read_in[2].get("telegram").get("bot").get("token")
