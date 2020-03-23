### Many thanks for inspiring me to 
 * **Nazmus Nasir** https://www.easyprogramming.net, https://github.com/naztronaut
 * **John Simmons** https://github.com/johndavidsimmons
 * **Felix Stern** https://tutorials-raspberrypi.de
---

# LedPiBot ![release](https://img.shields.io/github/release/kaulketh/ledpibot.svg?color=darkblue)
![size](https://img.shields.io/github/repo-size/kaulketh/ledpibot.svg?color=blue) ![commit](https://img.shields.io/github/last-commit/kaulketh/ledpibot.svg?color=darkviolet) ![platform](https://img.shields.io/badge/platform-linux-blue.svg?color=yellow) ![languages](https://img.shields.io/github/languages/count/kaulketh/ledpibot.svg?color=yellowgreen) ![coverage](https://img.shields.io/github/languages/top/kaulketh/ledpibot.svg?color=darkgreen&style=flat) [![license](https://img.shields.io/github/license/kaulketh/ledpibot.svg?color=darkred)](https://unlicense.org/)<br>
With this bot it is possible to control 24 artificial candles, in this case a wooden wreath is used and animated. 

Refer [Hardware description](./hardware/HARDWARE.md) and see some [impressions](hardware/media).
![wooden wreath](hardware/media/wreath.jpg) 

### Apart from default packages following is required additionally
* gcc , make, build-essential, python-dev, git, scons, swig
* from https://github.com/jgarff/rpi_ws281x clone, compile/build/install neopixel package 
* telepot as Python framework, https://telepot.readthedocs.io/en/latest/reference.html
* logrotate

### Enable [run at bootup](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#local)
````bash
# Edit rc.local 
sudo nano /etc/rc.local
# Insert 
sudo python3 /home/pi/bot.py &
````


[![license](https://img.shields.io/github/license/kaulketh/ledpibot.svg?color=darkred)](https://unlicense.org/)<br>
[LICENSE](https://github.com/kaulketh/ledpibot/blob/master/LICENSE) / [UNLICENSE](https://github.com/kaulketh/ledpibot/blob/master/UNLICENSE)