from .logger import PreconfiguredLogger

LOGGER = PreconfiguredLogger.instance
"""
preconfigured Singleton logger instance
"LedPi", 
../logs/debug.log (if enabled),  
../logs/info.log, 
../logs/error.log. 
"""
