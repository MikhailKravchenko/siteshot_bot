import logging.config
import logging
from pythonjsonlogger import jsonlogger


"""
§¯§Ñ§ã§ä§â§à§Û§Ü§Ñ logger  §Ú §æ§à§â§Þ§Ñ§ä§Ñ §ã§à§à§Ò§ë§Ö§ß§Ú§Û §Õ§Ý§ñ §Ý§à§Ô§Ñ JSON. §£§ã§Ö §Ù§Ñ§á§â§Ñ§ê§Ú§Ó§Ñ§Ö§ä§ã§ñ §Ú§Ù §æ§Ñ§Û§Ý§Ñ §Ü§à§æ§Ú§Ô§å§â§Ñ§è§Ú§Ú logging-json.ini
"""
logger = logging.getLogger(__name__)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
answerlog = logging.config.fileConfig('/src/logging-json.ini', disable_existing_loggers=False)
