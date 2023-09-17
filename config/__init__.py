#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

from .app_settings import *
from .dictionary import *
from .hw_settings import *
from .secret import *  # no public deployment!

build_text_libraries()
set_language(LANGUAGE)

m_wrong_id, m_not_allowed, m_pls_select, m_called, m_started, m_rebooted, \
    m_restarted, m_stopped, m_standby, m_stop_f, m_killed, \
    m_updated = get_texts(MSG)

commands = get_texts(CMD)
