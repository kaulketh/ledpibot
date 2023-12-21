## Operation Manual
Note: The authorized Telegram chat ID(s) and bot token are stored in a hidden file (secret.py) that is not provided here, but is imported or used at runtime.
    
* **Important Settings (_config/settings.py_):**
    Set chat language, possible language keys: "de", "en", "fr" <br>Only the chat language can set, logging and service functionality and related messages are hard coded in English.
    ````python script
    LANGUAGE = "de"
    ````    
    Auto reboot 1 minute after specified time if enabled    
    ````python script
    AUTO_REBOOT_ENABLED = False
    AUTO_REBOOT_TIME = "00:30"
    ````
    Auto brightness: Settings to reduce brightness of the LEDs due given period
    ````python script
    LED_DAY_BRIGHTNESS = 150
    LED_NIGHT_BRIGHTNESS = 70
    LED_MORNING_CUT_OFF = 8
    LED_NIGHT_CUT_OFF = 18
    ````


* **Main mode (run script _bot.py_)**
    * All settings are read/imported and set
    * Dictionaries are built (i.e. for functions to call)
    * Labels for buttons and message texts are loaded
    * Bot will inform user that it is ready to use via message
    * Use in-app command **/start** to start
    * Bot welcomes the user
    * Select any function/color to run
    * Bot answers with called function
    * Keyboard changes to stop-button keyboard
        * User is able to stop the running function
    * It is possible to call in-app commands at any time!
        * In-app commands have to declare via BotFather in the app
            * **/start**
            * **/stop**
            * **/service**
            * **/help**
        * **Call of a built-in command will break any running function!**
* **Functions/Animations:**
    * _**Clocks**_
        * **Clock 1** One LED per 'watch hand', red hour hand, blue minute hand, warm yellow running second hand every 2.5 seconds.One LED per 'watch hand', red hour hand, blue minute hand, warm yellow running second hand every 2.5 seconds.
        * **Clock 2** One LED per 'watch hand', red hour, blue minute, blue running light every 2.5 minutes from the current 'minute' to the '12'. 
        * **Clock 3** One LED per 'watch hand', red hour, blue minute, green seconds 'scale' will extend every 2.5 seconds. There is also a 'dial', subtly warm yellow for each 'number'.
        * **Clock 4** Colorful, full color 'watch face' for minute, hour, second, 'scales' will be overridden and colors mixed/changed thus. 
        * **Clock 5** Red hour hand, blue minute hand and warm yellow second 'pendulum' over all LEDs.
        * **Clock 6** Similar Clock 4, but w/o seconds and Green and Blue as major colors.
        * **Clock 7** white minute hand from LED 1 to 12 in 5 min steps (right half of circle), blue hour hand from LED 12 to 24 (left half of circle)
    * _**Colorful animations**_
        * All LEDs at once can switch to: **red**, **blue**, **green**, **white**, **yellow**, **orange**, **violet**
        * **Colors**: Switching simple colors in random time periods
        * **Colors II**: Fading over simple colors in random time periods
        * **Rainbow**: Rainbow animation with circular fading effect
        * **Rainbow II**: Rainbow animation with chaser, included fading effect.
        * **Theater**: Extremely colorful animation with spinning and wiping effects
        * **Theater II**: Another colorful animation with spinning effects
    * **Advent**: Advent calendar, works in Advent time only! For every day of December will one LED flicker like a candlelight. If it is Advent Sunday it flickers red. Should be time before December but in Advent period all LEDs are working as candlelight. If it is other than Advent time LEDs will circle in orange as warning!  
    * **Candles**: Each LED simulates candlelight
    * **Strobe**: Emitting brief and rapid flashes of white light in random frequency
* **Service menu** no app-in menu, will build due runtime but will be handled like an app-in command because of the slash in front 
    * **/Reboot** - What should I write here?
    * **/Info** - Information about the latest commit/release versions on GitHub, host name, IP, memory usage, disk usage, cpu load
    * **/Update** - Force update from GitHub to the latest version in master branch
    * **/Help** - Short version of this manual
* **Logging:**
    * Folder _**logs**_ in project root (if not exists will be created)
    * Log level DEBUG is shown in terminal/console (_stdout_)
    * Log level INFO is logged into _**logs/info.log**_
    * logs level ERROR is logged into _**logs/error.log**_
