#!/usr/bin/python3
# -*- coding: utf-8 -*-

from __future__ import annotations

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer__ = "Thomas Kaulke"
__status__ = "Production"

import os
from dataclasses import dataclass
from typing import Dict, Any, List

import yaml

from logger import LOGGER


# ---------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------
@dataclass
class SettingEntry:
    value: Any
    comment: str | None = None


@dataclass
class Settings:
    entries: Dict[str, SettingEntry]

    @classmethod
    def from_yaml(cls, data: dict):
        return cls(entries={k: SettingEntry(**v) for k, v in data.items()})

    def __getattr__(self, item):
        if item in self.entries:
            return self.entries[item].value
        raise AttributeError(item)


@dataclass
class ContentEntry:
    key: int
    type: str
    name: str
    translations: Dict[str, str]

    @classmethod
    def from_yaml(cls, key: str, data: dict):
        translations = {
            k: v for k, v in data.items()
            if k not in ("type", "name")
        }
        return cls(
            key=int(key),
            type=data["type"],
            name=data["name"],
            translations=translations
        )


@dataclass
class Contents:
    entries: List[ContentEntry]

    @classmethod
    def from_yaml(cls, data: dict):
        return cls(
            entries=[ContentEntry.from_yaml(k, v) for k, v in data.items()])


@dataclass
class Secrets:
    telegram_chat_thk: str
    telegram_bot_token: str

    @classmethod
    def from_yaml(cls, data: dict):
        tg = data["telegram"]
        return cls(
            telegram_chat_thk=tg["chat_ids"]["thk"],
            telegram_bot_token=tg["bot"]["token"]
        )


# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------
def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------
# Load YAML files
# ---------------------------------------------------------
here = os.path.dirname(os.path.abspath(__file__))

CFG_FILES = {
    "settings": "settings.yaml",
    "contents": "contents.yaml",
    "secrets": "secrets.yaml",
}

raw_settings = load_yaml(os.path.join(here, CFG_FILES["settings"]))
raw_contents = load_yaml(os.path.join(here, CFG_FILES["contents"]))
raw_secrets = load_yaml(os.path.join(here, CFG_FILES["secrets"]))
LOGGER.debug("All configuration files have been loaded")

# ---------------------------------------------------------
# Instantiate Dataclasses
# ---------------------------------------------------------
settings = Settings.from_yaml(raw_settings)
contents = Contents.from_yaml(raw_contents)
secrets = Secrets.from_yaml(raw_secrets)

# ---------------------------------------------------------
# Create dynamic global variables for settings (compat mode)
# ---------------------------------------------------------
for name, entry in settings.entries.items():
    globals()[name] = entry.value
    LOGGER.debug(f"apply setting {name} = {entry.value}")

# language from settings
language = settings.language

# ---------------------------------------------------------
# Create dynamic text variables + commands list
# ---------------------------------------------------------
texts: Dict[str, str] = {}
commands: List[str] = []

for entry in contents.entries:
    text_value = entry.translations.get(language)

    if not isinstance(text_value, str):
        LOGGER.error(f"Missing translation for '{entry.name}' in '{language}'")
        continue

    # create global variables
    globals()[entry.name] = text_value
    texts[entry.name] = text_value

    # commands list
    if entry.type == "btn_txt":
        commands.append(text_value.title())

    LOGGER.debug(
        f"setup {entry.type}[{entry.key:02d}] {entry.name} = {text_value.replace(chr(10), '')}")

# ---------------------------------------------------------
# Secrets
# ---------------------------------------------------------
ID_CHAT_THK = secrets.telegram_chat_thk
TOKEN_TELEGRAM_BOT = secrets.telegram_bot_token
