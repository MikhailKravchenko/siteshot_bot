import asyncio
import functools
import logging
import time
from datetime import datetime


def create_logger():
    """
    Создаем logger и возвращаем его
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # Файл для логов
    fh = logging.FileHandler("/src/log/siteshot_worklog.log")

    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def exception(function):
    """
    Декоратор для логирования исключений
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
    Декоратор для логирования времени работы обычных функций и методов
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
    Декоратор для логирования времени работы обычных функций и методов в котрых есть message: telebot.types.Message
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
    Декоратор для логирования времени работы асинхронных функций и методов
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
    Декоратор для логирования времени работы асинхронных функций и методов в котрых есть message: telebot.types.Message
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
    Декоратор для логирования времени работы асинхронных функций и методов в котрых есть telebot.types.CallbackQuery
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
