#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author___ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"
__maintainer___ = "Thomas Kaulke"
__status__ = "Development"


def test_audio(chat_id, bot):
    audio = ('advent', open('./sounds/calender_de.mp3', 'rb'))
    print(audio)
    bot.sendVoice(chat_id=chat_id, voice=audio, caption='Advent')
