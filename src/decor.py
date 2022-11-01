# -*- coding: utf-8 -*-
import functools
import logging
import time
from datetime import datetime
from typing import Any, Callable, Dict, Tuple


def create_logger() -> object:
    """
    Create a logger and return it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)

    # Файл для логов
    fh = logging.FileHandler("/src/log/siteshot_worklog.log")

    format_message: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_message)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


def exception(function: Callable) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
    """
    Decorator for logging exceptions
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except BaseException:
            # log the exception
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)

            # re-raise the exception
            raise

    return wrapper


def info_log(function: Callable) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
    """
    Decorator for logging the running time of regular functions and methods
    """

    def wrapper(*args, **kwargs) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
        starttime = time.time()
        res = function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        log_dict = {"facility": function.__name__, "run_duration": float(duration)}
        logging.info(function.__name__, extra=log_dict)
        return res

    return wrapper


def info_log_message(function: Callable) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
    """
    Decorator for logging the operation time of ordinary functions and methods
     in which there is a message: telebot.types.Message
    """

    def wrapper(*args, **kwargs) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
        starttime = time.time()
        if args[1].chat.first_name:
            first_name = args[1].chat.first_name
        else:
            first_name = args[1].from_user.first_name
        res = function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        log_dict = {'facility': function.__name__, "run_duration": float(duration),
                    'user.id': str(args[1].from_user.id),
                    'first_name': str(first_name),
                    'text': str(args[1].text),
                    'time_answer':
                        str(datetime.utcfromtimestamp(args[1].date).strftime('%Y-%m-%d %H:%M:%S'))}
        logging.info('System log', extra=log_dict)
        return res

    return wrapper


def info_log_async(function: Callable) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
    """
    Decorator for logging the running time of asynchronous functions and methods
    """

    async def wrapper(*args, **kwargs) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
        starttime = time.time()
        res = await function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        log_dict = {"facility": function.__name__, "run_duration": float(duration)}
        logging.info(function.__name__, extra=log_dict)
        return res

    return wrapper


def info_log_message_async(function: Callable) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
    """
    Decorator for logging the running time of asynchronous functions and methods
    in which there is a message: telebot.types.Message
    """

    async def wrapper(*args, **kwargs) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
        starttime = time.time()
        if args[1].chat.first_name:
            first_name = args[1].chat.first_name
        else:
            first_name = args[1].from_user.first_name
        res = await function(*args, **kwargs)
        endtime = time.time()
        duration = endtime - starttime
        log_dict = {'facility': function.__name__, "run_duration": float(duration),
                    'user.id': str(args[1].from_user.id),
                    'first_name': str(first_name),
                    'text': str(args[1].text),
                    'time_answer':
                        str(datetime.utcfromtimestamp(args[1].date).strftime('%Y-%m-%d %H:%M:%S'))}
        logging.info('System log', extra=log_dict)
        return res

    return wrapper


def info_log_message_async_callback(function: Callable) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
    """
    Decorator for logging the running time of asynchronous functions and methods that have telebot.types.CallbackQuery
    """

    async def wrapper(*args, **kwargs) -> Callable[[Tuple[Any, ...], Dict[str, Any]], Any]:
        starttime = time.time()
        if args[0].message.chat.first_name:
            first_name = args[0].message.chat.first_name
        else:
            first_name = args[0].message.from_user.first_name
        res = await function(*args)
        endtime = time.time()
        duration = endtime - starttime
        log_dict = {'facility': function.__name__, "run_duration": float(duration),
                    'user.id': str(args[0].message.from_user.id), 'first_name': str(first_name),
                    'text': str(args[0].message.text),
                    'time_answer':
                        str(datetime.utcfromtimestamp(args[0].message.date).strftime('%Y-%m-%d %H:%M:%S'))}
        logging.info('System log', extra=log_dict)
        return res

    return wrapper
