import asyncio
import functools
import logging
import time
from datetime import datetime


def create_logger():
    """
    §³§à§Ù§Õ§Ñ§Ö§Þ logger §Ú §Ó§à§Ù§Ó§â§Ñ§ë§Ñ§Ö§Þ §Ö§Ô§à
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler("/src/log/siteshot_worklog.log")

    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def exception(function):
    """
    §¥§Ö§Ü§à§â§Ñ§ä§à§â §Õ§Ý§ñ §Ý§à§Ô§Ú§â§à§Ó§Ñ§ß§Ú§ñ §Ú§ã§Ü§Ý§ð§é§Ö§ß§Ú§Û
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            # log the exception
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)

            # re-raise the exception
            raise

    return wrapper


def info_log(function):
    """
    §¥§Ö§Ü§à§â§Ñ§ä§à§â §Õ§Ý§ñ §Ý§à§Ô§Ú§â§à§Ó§Ñ§ß§Ú§ñ §Ó§â§Ö§Þ§Ö§ß§Ú §â§Ñ§Ò§à§ä§í §à§Ò§í§é§ß§í§ç §æ§å§ß§Ü§è§Ú§Û §Ú §Þ§Ö§ä§à§Õ§à§Ó
    """

    def wrapper(*args, **kwargs):
        starttime = time.time()
        res = function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        d = {"facility": function.__name__, "run_duration": float(duration)}
        logging.info(function.__name__, extra=d)
        return res

    return wrapper


def info_log_message(function):
    """
    §¥§Ö§Ü§à§â§Ñ§ä§à§â §Õ§Ý§ñ §Ý§à§Ô§Ú§â§à§Ó§Ñ§ß§Ú§ñ §Ó§â§Ö§Þ§Ö§ß§Ú §â§Ñ§Ò§à§ä§í §à§Ò§í§é§ß§í§ç §æ§å§ß§Ü§è§Ú§Û §Ú §Þ§Ö§ä§à§Õ§à§Ó §Ó §Ü§à§ä§â§í§ç §Ö§ã§ä§î message: telebot.types.Message
    """

    def wrapper(*args, **kwargs):
        starttime = time.time()
        if args[1].chat.first_name:
            first_name = args[1].chat.first_name
        else:
            first_name = args[1].from_user.first_name
        res = function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        d = {'facility': function.__name__, "run_duration": float(duration), 'user.id': str(args[1].from_user.id),
             'first_name': str(first_name),
             'text': str(args[1].text),
             'time_answer':
                 str(datetime.utcfromtimestamp(args[1].date).strftime('%Y-%m-%d %H:%M:%S'))}
        logging.info('System log', extra=d)
        return res

    return wrapper


def info_log_async(function):
    """
    §¥§Ö§Ü§à§â§Ñ§ä§à§â §Õ§Ý§ñ §Ý§à§Ô§Ú§â§à§Ó§Ñ§ß§Ú§ñ §Ó§â§Ö§Þ§Ö§ß§Ú §â§Ñ§Ò§à§ä§í §Ñ§ã§Ú§ß§ç§â§à§ß§ß§í§ç §æ§å§ß§Ü§è§Ú§Û §Ú §Þ§Ö§ä§à§Õ§à§Ó
    """

    async def wrapper(*args, **kwargs):
        starttime = time.time()
        res = await function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        d = {"facility": function.__name__, "run_duration": float(duration)}
        logging.info(function.__name__, extra=d)
        return res

    return wrapper


def info_log_message_async(function):
    """
    §¥§Ö§Ü§à§â§Ñ§ä§à§â §Õ§Ý§ñ §Ý§à§Ô§Ú§â§à§Ó§Ñ§ß§Ú§ñ §Ó§â§Ö§Þ§Ö§ß§Ú §â§Ñ§Ò§à§ä§í §Ñ§ã§Ú§ß§ç§â§à§ß§ß§í§ç §æ§å§ß§Ü§è§Ú§Û §Ú §Þ§Ö§ä§à§Õ§à§Ó §Ó §Ü§à§ä§â§í§ç §Ö§ã§ä§î message: telebot.types.Message
    """
    async def wrapper(*args, **kwargs):
        starttime = time.time()
        if args[1].chat.first_name:
            first_name = args[1].chat.first_name
        else:
            first_name = args[1].from_user.first_name
        res = await function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        d = {'facility': function.__name__, "run_duration": float(duration), 'user.id': str(args[1].from_user.id),
             'first_name': str(first_name),
             'text': str(args[1].text),
             'time_answer':
                 str(datetime.utcfromtimestamp(args[1].date).strftime('%Y-%m-%d %H:%M:%S'))}
        logging.info('System log', extra=d)
        return res

    return wrapper


def info_log_message_async_callback(function):
    """
    §¥§Ö§Ü§à§â§Ñ§ä§à§â §Õ§Ý§ñ §Ý§à§Ô§Ú§â§à§Ó§Ñ§ß§Ú§ñ §Ó§â§Ö§Þ§Ö§ß§Ú §â§Ñ§Ò§à§ä§í §Ñ§ã§Ú§ß§ç§â§à§ß§ß§í§ç §æ§å§ß§Ü§è§Ú§Û §Ú §Þ§Ö§ä§à§Õ§à§Ó §Ó §Ü§à§ä§â§í§ç §Ö§ã§ä§î telebot.types.CallbackQuery
    """
    async def wrapper(*args, **kwargs):
        starttime = time.time()
        if args[0].message.chat.first_name:
            first_name = args[0].message.chat.first_name
        else:
            first_name = args[0].message.from_user.first_name
        res = await function(*args)
        endtime = time.time()
        duration = endtime - starttime
        d = {'facility': function.__name__, "run_duration": float(duration),
             'user.id': str(args[0].message.from_user.id), 'first_name': str(first_name),
             'text': str(args[0].message.text),
             'time_answer':
                 str(datetime.utcfromtimestamp(args[0].message.date).strftime('%Y-%m-%d %H:%M:%S'))}
        logging.info('System log', extra=d)
        return res

    return wrapper
