# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime
from pyppeteer import launch
from decor import exception, info_log, info_log_message_async
from abstract import AbstractShooter, AbstractValidateUrl
from urllib.parse import urlparse


class ValidateUrl(AbstractValidateUrl):
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

    def __init__(self, url):
        self.url = url

    @info_log
    @exception
    def validate(self):
        if re.match(ValidateUrl.template_url_http, self.url) is not None:
            return True
        elif re.match(ValidateUrl.template_url, self.url) is not None:
            self.url = 'http://' + self.url
            return True
        else:
            return False
    @info_log
    @exception
    def parse_url(self):
        return urlparse(self.url).netloc


class Shooter(AbstractShooter):
    def __init__(self, message):
        self.message = message
        self._error = False

    @info_log_message_async
    async def get_screen_and_save_page(self, message, url, domen):
        starttime = time.time()
        # browser = await launch(executablePath='/usr/bin/google-chrome-stable', headless=True, args=['--no-sandbox'])
        browser = await launch()

        page = await browser.newPage()

        await page.setViewport({"width": 1200, "height": 1000})
        try:
            await page.goto(url)
        except:
            self._error = True
            return None, None, None, None
        filename = f'{datetime.utcfromtimestamp(message.date).strftime("%Y_%m_%d_%H_%M_%S")}_{message.chat.id}_{domen.replace(".", "_")}.png'
        file_path = 'storage/' + filename
        try:
            await page.screenshot({'path': file_path, })
        except:
            self._error = True
            return None, None, None, None
        title = await page.title()
        await browser.close()
        endtime = time.time()
        duration = endtime - starttime
        return filename, file_path, title, duration


class Statistic:

    def __init__(self, db_worker):
        self.db_worker = db_worker
        pass
    @info_log
    def get_statistic_for_admin(self):
        count_requests, count_success_requests, count_not_success_requests, top_domen, top_users = self.db_worker.get_statistic()
        text_url = ''
        for i, domen in enumerate(top_domen):
            text_url += f'{i + 1}. {domen[0]} количество запросов {domen[1]}\n'

        text_users = ''
        for i, user in enumerate(top_users):
            text_users += f'{i + 1}. ID: {user[0]}, username: {"отсутствует" if user[1] is None else user[1]},' \
                          f' first_name: {"отсутствует" if user[2] is None else user[2]},' \
                          f' количество запросов {user[3]}\n'
        text = f'Количество запросов за все время: {count_requests[0][0]}\n' \
               f'Удачных запросов: {count_success_requests[0][0]}\n' \
               f'Неудачных запросов: {count_not_success_requests[0][0]}\n' \
               f'Топ URL: \n{text_url}\n' \
               f'Топ пользователей:\n{text_users} '

        return text
