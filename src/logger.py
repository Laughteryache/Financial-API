from datetime import datetime
import logging

from pythonjsonlogger import jsonlogger

from src.config import settings

# Module for initializing the logger

logger = logging.getLogger()

logHandler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter()

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

formatter = CustomJsonFormatter(
    '%(timestamp)s %(level)s %(name)s %(message)s %(funcName)s815'
    )


logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)