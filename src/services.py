# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime
from typing import Tuple, Union
from urllib.parse import urlparse

import telebot
from pyppeteer import launch

from abstract import AbstractShooter, AbstractValidateUrl
from decor import exception, info_log, info_log_message_async


class ValidateUrl(AbstractValidateUrl):
    """
    Class for checking the validity of the URL and getting the domain from it
    """
    # Паттерны URL
    template_url_http = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    template_url = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self, url: str) -> None:
        self.url = url

    @info_log
    @exception
    def validate(self) -> bool:
        """
        Checking URl for a match with a pattern
        :return:
        """
        if re.match(ValidateUrl.template_url_http, self.url) is not None:
            return True
        elif re.match(ValidateUrl.template_url, self.url) is not None:
            self.url = 'http://' + self.url
            return True
        else:
            return False

    @info_log
    @exception
    def parse_url(self) -> str:
        """
        Parsing a domain from a URL
        :return:
        """
        return urlparse(self.url).netloc


class Shooter(AbstractShooter):
    """
    Class for getting a screenshot and saving it
     uses the pyppeteer library to open the browser and get the page image
    """

    def __init__(self) -> None:
        self._error = False

    @info_log_message_async
    async def get_screen_and_save_page(self, message: telebot.types.Message, url: str, domen: str) -> \
            Union[Tuple[None, None, None, None], Tuple[str, str, str, float]]:
        """
        The method opens the browser, configures the page settings, makes a request to the received URL,
         saves file to disk, returns filename, path, page title, runtime
         In case of an error, translates self._error = True and returns an empty result
        :param message:
        :param url:
        :param domen:
        :return:
        """
        starttime = time.time()
        browser = await launch(executablePath='/usr/bin/google-chrome-stable', headless=True, args=['--no-sandbox'])
        # browser = await launch()

        page = await browser.newPage()

        await page.setViewport({"width": 1200, "height": 1000})

        try:
            await page.goto(url)
        except BaseException:
            self._error = True
            return None, None, None, None
        filename = f'{datetime.utcfromtimestamp(message.date).strftime("%Y_%m_%d_%H_%M_%S")}_{message.chat.id}_{domen.replace(".", "_")}.png'
        file_path = 'storage/' + filename
        try:
            await page.screenshot({'path': file_path, })
        except BaseException:
            self._error = True
            return None, None, None, None
        title = await page.title()
        await browser.close()
        endtime = time.time()
        duration = endtime - starttime
        return filename, file_path, title, duration


class Statistic:
    """
   Class for processing raw statistics data obtained from the database
    """

    def __init__(self, db_worker: object) -> None:
        self.db_worker = db_worker

    @info_log
    def get_statistic_for_admin(self) -> str:
        """
        The method returns a string with bot statistics data
        :return:
        """
        count_requests, count_success_requests, count_not_success_requests, \
        top_domen, top_users, average_duration = self.db_worker.get_statistic()
        text_url = ''
        for i, domen in enumerate(top_domen):
            text_url += f'{i + 1}. {domen[0]} number of requests {domen[1]}\n'

        text_users = ''
        for i, user in enumerate(top_users):
            text_users += f'{i + 1}. ID: {user[0]}, username: {"None" if user[1] is None else user[1]},' \
                          f' first_name: {"None" if user[2] is None else user[2]},' \
                          f' number of requests {user[3]}\n'
        text = f'Number of requests for all time: {count_requests[0][0]}\n\n' \
               f'Successful Requests: {count_success_requests[0][0]}\n\n' \
               f'Failed Requests: {count_not_success_requests[0][0]}\n\n' \
               f'Top URL: \n{text_url}\n\n' \
               f'Top users:\n{text_users}\n' \
               f'Average query execution time in seconds: {"%.4f" % average_duration[0][0]}'
        return text
