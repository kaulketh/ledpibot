#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import json
import os

from logger import LOGGER
from .settings import *
from .secret import *  # no public deployment!

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, TRANSLATIONS), 'r', encoding='utf-8') as file:
    translations = json.load(file)

commands = []
# not really needed, but better to avoid error messages in the IDE
(m_wrong_id, m_not_allowed, m_pls_select, m_called, m_started, m_rebooted,
 m_restarted, m_stopped, m_standby, m_stop_f, m_killed, m_updated) \
    = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

LOGGER.debug(f"Dynamically creating variables")
for item in translations.items():
    _type = item[1].get('type')
    _name = item[1].get('name')
    _value = item[1].get(LANGUAGE)
    _n = item[0]
    globals()[_name] = _value
    if _type == "function":
        # commands
        _n = len(commands)
        commands.append(globals().get(_name).title())
    _value_r = _value.replace("\n", "")
    LOGGER.debug(f"{_type} {_n} '{_name}': '{_value_r}'")
