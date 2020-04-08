## Operation Manual
Note: Authorized Telegram Chat ID(s) and the bot token are stored in a hidden file(secret.py) which is not deployed and thence will be imported to access.py to import or use due runtime
    
* **Important Settings (_config/settings.py_):**
    Set chat language, possible language keys: "de", "de_emoji", "en", "en_emoji", "fr" <br>Only the chat language can set, logging and service functionality and related messages are hard coded in English.
    ````python script
    LANGUAGE = "de"
    ````    
    Auto Reboot: Reboot every day at given time (here 2:00 AM) if TRUE    
    ````python script
    AUTO_REBOOT_ENABLED = False
    AUTO_REBOOT_CLOCK_TIME = 2
    ````
    Auto brightness: Settings to reduce brighness of the LEDs due given period
    ````python script
    LED_DAY_BRIGHTNESS = 150
    LED_NIGHT_BRIGHTNESS = 70
    LED_MORNING_CUT_OFF = 8
    LED_NIGHT_CUT_OFF = 18
    ````
    Countdown functionality: Maximum runtime of function and waiting time (standby) until restart, remaining time until stop will be messaged if TRUE
    ````python script
    COUNTDOWN_MINUTES = (7 * 60)
    COUNTDOWN_RESTART_MINUTES = (17 * 60)
    COUNTDOWN_DISPLAY_REMAINING_TIME = False
    ````    

* **Main mode (run script _bot.py_)**
    * All settings are read/imported and set
    * Dictionaries are built (i.e. for functions to call)
    * Labels for buttons and message texts are loaded
    * Bot will inform user that it is ready to use via message
    * Use in-app command **/start** to start
    * Bot welcomes the user
    * Select any function/color to run
    * Bot messages about run and the clock time of auto-standby
    * Keyboard changes to 2-button keyboard (stop/standby)
        * User is able to stop the running function or to force standby
        * Bot messages the clock time of restart
    * When standby mode is reached only one stop button is displayed
        * User is able to break the running standby
    * It is possible to call in-app commands at any time!
        * In-app commands have to declare via BotFather in the app
            * **/start**
            * **/stop**
            * **/service**
        * **Call of an built-in command will break running function!**
* **Functions/Animations:**
    * _**Clocks**_
        * **Clock 1** One LED per "pointer", Red hours "pointer", blue minutes "pointer", warm yellow running seconds "pointer" every 2.5 seconds
        * **Clock 2** One LED per "pointer", Red hours "pointer", blue minutes "pointer", a blue running light every 2.5 minutes from the current "minute" to the "12" 
        * **Clock 3** One LED per "pointer", Red hours "pointer", blue minutes "pointer", green seconds "scale" will extends every 2.5 seconds, there is also a "dial", a subtly warm yellow LED on each "number".
        * **Clock 4** Colorful, full color "scale" to minute, hour, second, "scales" will overridden and colors mixed/changed thus 
        * **Clock 5** Red hours "pointer", blue minutes "pointer" and a warm yellow 1 second "pendulum" over all LEDs
    * **Advent**: Advent calendar, works in December only! For every day of December will one LED flickering like a candle light. If it is Advent Sunday it flickers red. If month is other than December all LEDs flickering in red as warning  
    * **Candles**: Each LED flickers like candle light
    * **Rainbow**: Rainbow animation with circular fading effect
    * **Theater**: Extremely colorful animation with chaser, spinning, wiping effects
    * **Strobe**: Emitting brief and rapid flashes of white light in random frequency
    * _**Colors**_
        * **Colors**: Switching simple colors in random time periods
        * **Colors 2**: Fading over simple colors in random time periods
        * All LEDs at once can switched to: **red**, **blue**, **green**, **white**, **yellow**, **orange**, **violet**
* **Service menu** no app-in menu, will build due runtime but will handled like a app-in command because of the slash in front 
    * **/Reboot** - What should I write here?
    * **/Info** - Information about latest commit/release verions on Github, host name, IP, memory usage, disk usage, cpu load
    * **/Update** - Force update from Github to the latest version in master branch
    * **/Help** - Short version of this manual
* **Logging:**
    * Folder _**logs**_ in project root (if not exists will be created)
    * Log level DEBUG is shown in terminal/console (_stdout_)
    * Log level INFO is logged into _**logs/info.log**_
    * logs level ERROR is logged into _**logs/error.log**_