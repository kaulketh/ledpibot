#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from .access import *
from .dictionary import *
from .secret import *
from .settings import *

build_dictionary()
set_language(LANGUAGE)

m_wrong_id, m_not_allowed, m_pls_select, m_called, m_started, m_rebooted, \
    m_rotated, m_stopped, m_standby, m_stop_f, m_killed, \
    m_updated = get_translations(MSG)

commands = get_translations(CMD)
