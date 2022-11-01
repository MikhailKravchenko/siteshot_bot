# -*- coding: utf-8 -*-
import logging
import logging.config

from pythonjsonlogger import jsonlogger

"""
Setting logger and message format for JSON log. Everything is requested from the configuration file logging-json.ini
"""
logger = logging.getLogger(__name__)
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)
answerlog = logging.config.fileConfig('/src/logging-json.ini', disable_existing_loggers=False)
