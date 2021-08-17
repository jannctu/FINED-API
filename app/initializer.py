class LoggerInstance(object):
    def __new__(cls):
        from app.modules.logger.custom_logging import LogHandler
        return LogHandler()

logger_instance = LoggerInstance()