# -*- coding: utf-8 -*-
import logging.config
import logging
from pythonjsonlogger import jsonlogger


"""
Настройка logger  и формата сообщений для лога JSON. Все запрашивается из файла кофигурации logging-json.ini
"""
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
answerlog = logging.config.fileConfig('/src/logging-json.ini', disable_existing_loggers=False)
