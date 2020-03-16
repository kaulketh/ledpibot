#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Production"

from .access import *
from .dictionary import *
from .secret import *
from .settings import *

set_language("de")

wrong_id, not_allowed, pls_select, called, started, rebooted, rotated, stopped, standby, stop_msg, killed, updated \
    = get_translations("message")

commands = get_translations("command")
