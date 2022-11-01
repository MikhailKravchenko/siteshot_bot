# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class AbstractCore(ABC):
    # Abstract class Core
    @abstractmethod
    async def get_data(self, request):
        pass

    @abstractmethod
    async def run(self):
        pass

    def run_webhook(self):
        pass


class AbstractPostgresQL(ABC):
    # Abstract class БД
    @abstractmethod
    def set_statistic_succses_true(self, message, url, domen, file_name, file_path, duration):
        pass

    @abstractmethod
    def set_statistic_succses_false(self, message, url, domen, file_name, file_path, duration):
        pass

    @abstractmethod
    def get_statistic(self):
        pass


class AbstractShooter(ABC):
    # Abstract class Shooter
    @abstractmethod
    async def get_screen_and_save_page(self, message, url, domen):
        pass


class AbstractValidateUrl(ABC):
    # Abstract class ValidateUrl
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def parse_url(self):
        pass
