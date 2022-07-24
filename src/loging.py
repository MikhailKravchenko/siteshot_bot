import logging.config
import logging
from pythonjsonlogger import jsonlogger


"""
���ѧ����ۧܧ� logger  �� ����ާѧ�� ����ҧ�֧ߧڧ� �էݧ� �ݧ�ԧ� JSON. ����� �٧ѧ��ѧ�ڧӧѧ֧��� �ڧ� ��ѧۧݧ� �ܧ��ڧԧ��ѧ�ڧ� logging-json.ini
"""
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
answerlog = logging.config.fileConfig('/src/logging-json.ini', disable_existing_loggers=False)
