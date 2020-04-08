### Operation Manual
    In this case are stored the allowed Telegram Chat ID(s) in a hidden file(_secret.py_) which is not deployed
    and thence will be imported to _access.py_ to import or use due runtime

* Important Settings (config/settings.py):
    ######Set chat language: posible language keys: "de", "de_emoji", "en", "en_emoji", "fr"
        LANGUAGE = "de" 
    ######Auto Reboot: Reboot every day at given time (here 2:00 AM) if TRUE    
        AUTO_REBOOT_ENABLED = False
        AUTO_REBOOT_CLOCK_TIME = 2
    ######Auto brightness: Settings to reduce brighness of the LEDs due given period
        LED_DAY_BRIGHTNESS = 150
        LED_NIGHT_BRIGHTNESS = 70
        LED_MORNING_CUT_OFF = 8
        LED_NIGHT_CUT_OFF = 18
    ######Countdown functionality: Maximum runtime of function and waiting time (standby) until restart, remaining time until stop will be messaged if TRUE
        COUNTDOWN_MINUTES = (7 * 60)
        COUNTDOWN_RESTART_MINUTES = (17 * 60)
        COUNTDOWN_DISPLAY_REMAINING_TIME = False

* Main mode (run script _bot.py_)
    * All settings rae read/imported and set
    * Dictionaries are built (i.e. for functions to call)
    * Labels for buttons and message texts are loaded
    * Bot will inform user that it is ready to use yia message
    * Use in-app command **/start** to start
    * Bot welcomes the user
    * Select any function/color to run
    * Bot messages about run and the clock time of auto-standby
    * Keyborad in app will be changed to 2-button keyboard (stop/standby)
        * User is able to stop the running function or to force a standby
        * Bot messages about the clock time of restart
    * When standby mode is reached only one stop button is displayed
        * User is able to break the running standby
    * It is possible to call in-app commands at any time!
        * In-app commands have to declare via BotFather in the app
            * **/start**
            * **/stop**
            * **/service**
        * **Call of an built-in command will break running function!**
* Service menu: 
    * **/Reboot** - What should I write here?
    * **/Info** - Information about latest commit/release verions on Github, host name, IP, memory usage, disk usage, cpu load
    * **/Update** - Force update from Github to the latest version in master branch
 
    
    
    