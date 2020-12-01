### Many thanks for inspiring me to 
 * **Nazmus Nasir** https://www.easyprogramming.net, https://github.com/naztronaut
 * **John Simmons** https://github.com/johndavidsimmons
 * **Felix Stern** https://tutorials-raspberrypi.de
 
---

# LedPiBot
![GitHub release (latest by date)](https://img.shields.io/github/v/release/kaulketh/ledpibot?color=red)![GitHub Release Date](https://img.shields.io/github/release-date/kaulketh/ledpibot?color=red&label= )![commit](https://img.shields.io/github/last-commit/kaulketh/ledpibot.svg?color=red) ![size](https://img.shields.io/github/repo-size/kaulketh/ledpibot.svg?color=blue) ![platform](https://img.shields.io/badge/platform-linux-blue.svg?color=yellow) ![languages](https://img.shields.io/github/languages/count/kaulketh/ledpibot.svg?color=yellowgreen) ![coverage](https://img.shields.io/github/languages/top/kaulketh/ledpibot.svg?color=darkgreen&style=flat) [![license](https://img.shields.io/github/license/kaulketh/ledpibot.svg?color=darkred)](https://unlicense.org/)<br>
<br>
### Summary
With this bot it is possible to control 24 artificial candles, in this case a wooden wreath is used and animated.
More information can be found in **[manual](MANUAL.md)**. 
Also refer **[hardware description](hardware/HARDWARE.md)** or look at some **[impressions](hardware/media)**.
<br><br>![wooden wreath](hardware/media/wreath.jpg) 
<br><br>
### Apart from default packages following is required additionally
* gcc , make, build-essential, python-dev, git, scons, swig
* rpi_ws281x from https://github.com/rpi-ws281x/rpi-ws281x-python
* Python frameworks for Telegram Bot API:
    * telepot, https://telepot.readthedocs.io/en/latest/reference.html
    * telegram, https://python-telegram-bot.org
* logrotate

### Enable [run at bootup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#systemd)
... to use the _systemd_ files. _systemd_ provides a standard process for controlling what programs run when a Linux system boots up. Note that _systemd_ is available only from the Jessie versions of Raspbian OS.


[![license](https://img.shields.io/github/license/kaulketh/ledpibot.svg?color=darkred)](https://unlicense.org/)<br>
[LICENSE](https://github.com/kaulketh/ledpibot/blob/master/LICENSE) / [UNLICENSE](https://github.com/kaulketh/ledpibot/blob/master/UNLICENSE)
