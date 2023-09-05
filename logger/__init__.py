from .logger import PreconfiguredLogger

LOGS = PreconfiguredLogger.log_folder
LOGGER = PreconfiguredLogger.instance
"""
preconfigured Singleton logger instance
"LedPi", 
../logs/debug.log (if enabled),  
../logs/info.log, 
../logs/error.log. 
"""
