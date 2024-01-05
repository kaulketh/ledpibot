from .logger import PreconfiguredLogger

# instantiate logger
LOGGER = PreconfiguredLogger.instance
"""preconfigured Singleton logger instance, for settings refer 'logger.yaml'"""

HISTORY = PreconfiguredLogger.HIS_LOG
LOGS = PreconfiguredLogger.log_folder
