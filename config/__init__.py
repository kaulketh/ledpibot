#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import json
import os

from logger import LOGGER
from .secret import *  # no public deployment!

HERE = os.path.dirname(os.path.abspath(__file__))
SETUP = "settings.json", "ui_translations.json"

# load settings and UI contents
with open(os.path.join(HERE, SETUP[0]), 'r', encoding='utf-8') as file:
    settings = json.load(file)

with open(os.path.join(HERE, SETUP[1]), 'r', encoding='utf-8') as file:
    translations = json.load(file)

# init empty variables to avoid "Unresolved reference" errors in IDE
(led_count, led_pin, led_freq_hz, led_dma, led_brightness, led_invert,
 led_brightness_day, led_brightness_night, led_cut_off_morning,
 led_cut_off_night, auto_reboot_enabled, auto_reboot_time, auto_reboot_msg,
 auto_start, auto_start_msg, language, running) \
    = [None] * 17
(m_wrong_id, m_not_allowed, m_pls_select, m_called, m_started, m_rebooted,
 m_restarted, m_stopped, m_standby, m_stop_f, m_killed, m_updated) \
    = [None] * 12

# define variables dynamically (settings first!)
# settings
for item in settings.items():
    _name = item[0]
    _value = item[1].get("value")
    _com = item[1].get("comment")
    globals()[_name] = _value  # variables creation dynamically
    LOGGER.debug(f"setting {_name} = {_value}")

# texts
commands = []
for item in translations.items():
    _type = item[1].get('type')
    _name = item[1].get('name')
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
