from abc import ABC

import psycopg2 as psycopg2

from siteshot_bot import env
from siteshot_bot.abstract import AbstractPostgresQL


class PostgreSQL(AbstractPostgresQL):
    def __init__(self):
        self.connection = psycopg2.connect(user=env.DATABASE_USERNAME,
                                           password=env.DATABASE_PASSWORD,
                                           host=env.DATABASE_HOST,
                                           port=env.DATABASE_PORT,
                                           database=env.DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def get_statistic(self):
        pass

    def set_statistic(self):
        pass