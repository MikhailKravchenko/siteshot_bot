# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime
from urllib.parse import urlparse
import telebot
from pyppeteer import launch
from decor import exception, info_log, info_log_message_async
from abstract import AbstractShooter, AbstractValidateUrl



class ValidateUrl(AbstractValidateUrl):
    """
    Класс для проверки валидности URL и получения из него домена
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

    def __init__(self, url):
        self.url = url

    @info_log
    @exception
    def validate(self) -> bool:
        """
        Проверка URl на совпадение с паттерном
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
        Парсинг домена из URL
        :return:
        """
        return urlparse(self.url).netloc


class Shooter(AbstractShooter):
    """
    Класс для получения скрина и его сохранения
    использует библиотеку pyppeteer для открытия браузера и получения изображения страницы
    """

    def __init__(self):
        self._error = False

    @info_log_message_async
    async def get_screen_and_save_page(self, message: telebot.types.Message, url: str, domen: str):
        """
        Метод открывает браузер, настраивает параметры страницы, делает запрос по полученному URL,
        сохраняет файл на диск, возвращает имя файла, путь, название страницы, время выполнения
        В случае ошибки переводит self._error = True  и возвращает пустой результат
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
    """
    Класс для обработки сырых данных статистики полученой из БД
    """

    def __init__(self, db_worker):
        self.db_worker = db_worker


    @info_log
    def get_statistic_for_admin(self) -> str:
        """
        Метод возвращает строку с данными статистики работы бота
        :return:
        """
        count_requests, count_success_requests, count_not_success_requests, \
        top_domen, top_users, average_duration = self.db_worker.get_statistic()
        text_url = ''
        for i, domen in enumerate(top_domen):
            text_url += f'{i + 1}. {domen[0]} количество запросов {domen[1]}\n'

        text_users = ''
        for i, user in enumerate(top_users):
            text_users += f'{i + 1}. ID: {user[0]}, username: {"отсутствует" if user[1] is None else user[1]},' \
                          f' first_name: {"отсутствует" if user[2] is None else user[2]},' \
                          f' количество запросов {user[3]}\n'
        text = f'Количество запросов за все время: {count_requests[0][0]}\n\n' \
               f'Удачных запросов: {count_success_requests[0][0]}\n\n' \
               f'Неудачных запросов: {count_not_success_requests[0][0]}\n\n' \
               f'Топ URL: \n{text_url}\n\n' \
               f'Топ пользователей:\n{text_users}\n' \
               f'Среднее время выполнения запроса: {"%.4f" % average_duration[0][0]} сек.'
        return text
