# -*- coding: utf-8 -*-
import re
import time
from datetime import datetime
from pyppeteer import launch

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

    def validate(self):
        if re.match(ValidateUrl.template_url_http, self.url) is not None:
            return True
        elif re.match(ValidateUrl.template_url, self.url) is not None:
            self.url = 'http://' + self.url
            return True
        else:
            return False

    def parse_url(self):
        return urlparse(self.url).netloc


class Shooter(AbstractShooter):
    def __init__(self, message):
        self.message = message
        self._error = False

    async def get_screen_and_save_page(self, message, url, domen):
        starttime = time.time()
        browser = await launch(executablePath='/usr/bin/google-chrome-stable', headless=True, args=['--no-sandbox'])
        # browser = await launch()

        page = await browser.newPage()

        await page.setViewport({"width": 1200, "height": 1000})
        try:
            await page.goto(url)
        except:
            self._error = True
            return None, None, None
        filename = f'storage/{datetime.utcfromtimestamp(message.date).strftime("%Y_%m_%d_%H_%M_%S")}_{message.chat.id}_{domen.replace(".", "_")}.png'
        try:
            await page.screenshot({'path': filename, })
        except:
            self._error = True
            return None, None, None
        title = await page.title()
        await browser.close()
        endtime = time.time()
        duration = endtime - starttime
        return filename, title, duration
