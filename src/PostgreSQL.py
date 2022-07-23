# -*- coding: utf-8 -*-
import sys
import time
from datetime import datetime

from loging import logging

import psycopg2 as psycopg2
from env import *
from abstract import AbstractPostgresQL


class PostgreSQL(AbstractPostgresQL):
    def __init__(self):
        self.connection = psycopg2.connect(user=DATABASE_USERNAME,
                                           password=DATABASE_PASSWORD,
                                           host=DATABASE_HOST,
                                           port=DATABASE_PORT,
                                           database=DATABASE_NAME)
        self.cursor = self.connection.cursor()

    def set_user_info_in_db(self, message):

        starttime = time.time()
        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO users (user_id, user_name, first_name) VALUES (%s, %s, %s)",
                    (str(message.chat.id), str(message.chat.username), str(first_name)))
            except Exception as e:
                return False

            endtime = time.time()
            duration = endtime - starttime
            d = {"facility": sys._getframe().f_code.co_name, "run_duration": duration, "user.id": str(
                message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}

            logging.info('SQL', extra=d)
            return True

    def update_user_in_db(self, message):
        starttime = time.time()
        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        with self.connection:
            try:
                self.cursor.execute(
                    "UPDATE users SET user_name = %s, first_name=%s WHERE user_id = %s",
                    (str(message.chat.username), str(first_name), str(message.chat.id)))
            except Exception as e:
                d = {"facility": sys._getframe().f_code.co_name, "exception": e, "user.id": str(
                    message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                    datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}
                logging.error('SQL', extra=d)
        endtime = time.time()
        duration = endtime - starttime
        d = {"facility": sys._getframe().f_code.co_name, "run_duration": duration, "user.id": str(
            message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
            datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}

        logging.info('SQL', extra=d)

    def get_statistic(self):
        with self.connection:
            self.cursor.execute('SELECT COUNT(*) FROM request')
            count_requests = self.cursor.fetchall()
            self.cursor.execute('SELECT COUNT(*) FROM request WHERE success is true')
            count_success_requests = self.cursor.fetchall()
            self.cursor.execute('SELECT COUNT(*) FROM request WHERE success is false')
            count_not_success_requests = self.cursor.fetchall()
            self.cursor.execute('SELECT domen, COUNT(*) FROM request group by domen ORDER BY COUNT DESC  LIMIT 10')
            top_domen = self.cursor.fetchall()
            self.cursor.execute('SELECT  request.user_id,users.user_name, users.first_name,  COUNT(*)  FROM request  JOIN users ON request.user_id = users.user_id group by request.user_id, users.user_name, users.first_name ORDER BY COUNT DESC  LIMIT 10')

            top_users = self.cursor.fetchall()
            return count_requests, count_success_requests, count_not_success_requests, top_domen, top_users

    def set_statistic_succses_true(self, message, url, domen, file_name, file_path, duration):

        starttime = time.time()
        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO request (url, domen, success, user_id, file_name,file_path, duration) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                    (str(url), str(domen), True, str(message.chat.id), str(file_name), str(file_path), int(duration)))
            except Exception as e:
                d = {"facility": sys._getframe().f_code.co_name, "exception": e, "user.id": str(
                    message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                    datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}
                logging.error('SQL', extra=d)
                return False

            endtime = time.time()
            duration = endtime - starttime
            d = {"facility": sys._getframe().f_code.co_name, "run_duration": duration, "user.id": str(
                message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}

            logging.info('SQL', extra=d)
            return True

    def set_statistic_succses_false(self, message, url, domen, file_name, file_path, duration):
        starttime = time.time()
        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO request (url, domen, success, user_id, file_name,file_path, duration) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                    (str(url), str(domen), False, str(message.chat.id), file_name, file_path, duration))
            except Exception as e:
                d = {"facility": sys._getframe().f_code.co_name, "exception": e, "user.id": str(
                    message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                    datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}
                logging.error('SQL', extra=d)
                print(e)
                return False

            endtime = time.time()
            duration = endtime - starttime
            d = {"facility": sys._getframe().f_code.co_name, "run_duration": duration, "user.id": str(
                message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}

            logging.info('SQL', extra=d)
            return True

    def get_admin_chat_id(self):
        with self.connection:
            self.cursor.execute('SELECT chat_id FROM admin_chat')
            chat_id = self.cursor.fetchall()
            return chat_id

    def set_admin_chat_in_db(self, message):

        starttime = time.time()
        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO admin_chat (chat_id) VALUES (%s)",
                    (str(message.chat.id),))
            except Exception as e:
                d = {"facility": sys._getframe().f_code.co_name, "exception": e, "user.id": str(
                    message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                    datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}
                logging.error('SQL', extra=d)
                return False

            endtime = time.time()
            duration = endtime - starttime
            d = {"facility": sys._getframe().f_code.co_name, "run_duration": duration, "user.id": str(
                message.from_user.id), "first_name": str(first_name), "text": str(message.text), "time_answer": str(
                datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}

            logging.info('SQL', extra=d)
            return True
