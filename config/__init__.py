#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

from .access import *
from .dictionary import get_translations, set_language
from .secret import *
from .settings import *

set_language(LANGUAGE)

m_wrong_id, m_not_allowed, m_pls_select, m_called, m_started, m_rebooted, \
m_rotated, m_stopped, m_standby, m_stop_f, m_killed, \
m_updated = get_translations("message")

commands = get_translations("command")
