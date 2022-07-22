import asyncio
import platform
import re
from datetime import datetime

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from siteshot_bot.abstract import AbstractShooter, AbstractValidateUrl
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
        return urlparse(self.url).netloc.split('.')


class Shooter(AbstractShooter):
    def __init__(self, message):
        self.chrome_options = webdriver.ChromeOptions()
        self.message = message
        self._error = False

    async def get_screen_page(self, url):
        self.chrome_options.headless = True
        # ������ �� ��֧اڧ� �ڧߧܧ�ԧߧڧ��
        self.chrome_options.add_argument("--incognito")
        # ���էڧߧѧܧ�ӧ�� �է֧ۧ��ӧڧ� �� �٧ѧӧڧ�ڧާ���� ��� ����. ���ߧڧ�ڧѧݧڧ٧ѧ�ڧ� ���֧ҧ���ѧۧӧ֧��
        await asyncio.sleep(0)

        if platform.uname().system in ('Linux', 'Darwin'):

            self.driver = webdriver.Chrome('/usr/bin/chromedriver', options=self.chrome_options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options)
        # ����ܧ���ڧ� �� �٧ѧԧ��٧ܧ� ����ѧߧڧ��
        S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
        self.driver.set_window_size(S('Width'), ('1080'))
        await asyncio.sleep(0)

        try:
            self.driver.get(url)

        except:
            self._error = True
            return
        await asyncio.sleep(0)

    async def save_screen(self, message, url, domen):
        await asyncio.sleep(0)
        self.driver.save_screenshot(
            f'./storage/{datetime.utcfromtimestamp(message.date).strftime("%Y_%m_%d_%H_%M_%S")}_{message.chat.id}_{domen}.png')
