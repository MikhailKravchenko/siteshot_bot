# -*- coding: utf-8 -*-
import psycopg2 as psycopg2
import telebot

from abstract import AbstractPostgresQL
from decor import exception, info_log, info_log_message
from env import (
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USERNAME,
)


class PostgreSQL(AbstractPostgresQL):
    """
    Класс для доступа в БД
    """

    def __init__(self) -> None:
        self.connection = psycopg2.connect(user=DATABASE_USERNAME,
                                           password=DATABASE_PASSWORD,
                                           host=DATABASE_HOST,
                                           port=DATABASE_PORT,
                                           database=DATABASE_NAME)
        self.cursor = self.connection.cursor()

    @info_log_message
    @exception
    def set_user_info_in_db(self, message: telebot.types.Message) -> bool:
        """
        Добавляет информацию о пользователе в БД
        :param message:
        :return:
        """
        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO users (user_id, user_name, first_name) VALUES (%s, %s, %s)",
                    (str(message.chat.id), str(message.chat.username), str(first_name)))
            except Exception:
                return False

            return True

    @info_log_message
    @exception
    def update_user_in_db(self, message: telebot.types.Message) -> bool:
        """
        Метод обновляет информацию о пользователе в БД
        :param message:
        :return:
        """
        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        with self.connection:
            self.cursor.execute(
                "UPDATE users SET user_name = %s, first_name=%s WHERE user_id = %s",
                (str(message.chat.username), str(first_name), str(message.chat.id)))
        return True

    @info_log
    @exception
    def get_statistic(self) -> list:
        """
        Получение данных статистики из БД
        :return:
        """
        with self.connection:
            self.cursor.execute('SELECT COUNT(*) FROM request')
            count_requests = self.cursor.fetchall()
            self.cursor.execute('SELECT COUNT(*) FROM request WHERE success is true')
            count_success_requests = self.cursor.fetchall()
            self.cursor.execute('SELECT COUNT(*) FROM request WHERE success is false')
            count_not_success_requests = self.cursor.fetchall()
            self.cursor.execute('SELECT domen, COUNT(*) FROM request group by domen ORDER BY COUNT DESC  LIMIT 10')
            top_domen = self.cursor.fetchall()
            self.cursor.execute(
                'SELECT  request.user_id,users.user_name, users.first_name,  COUNT(*)  FROM request  JOIN users ON request.user_id = users.user_id group by request.user_id, users.user_name, users.first_name ORDER BY COUNT DESC  LIMIT 10')
            top_users = self.cursor.fetchall()
            self.cursor.execute('SELECT AvG(duration) AS durAvg FROM request')
            average_duration = self.cursor.fetchall()
            return count_requests, count_success_requests, count_not_success_requests, top_domen, top_users, average_duration

    @info_log_message
    @exception
    def set_statistic_succses_true(self, message: telebot.types.Message, url: str, domen: str, file_name: str,
                                   file_path: str, duration: float) -> bool:
        """
        Создание записи в таблицу статистики об удачном выполнении запроса
        :param message:
        :param url:
        :param domen:
        :param file_name:
        :param file_path:
        :param duration:
        :return:
        """

        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO request (url, domen, success, user_id, file_name,file_path, duration) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                    (str(url), str(domen), True, str(message.chat.id), str(file_name), str(file_path), int(duration)))
            except Exception:

                return False

            return True

    @info_log_message
    @exception
    def set_statistic_succses_false(self, message: telebot.types.Message, url: str, domen: str, file_name: None,
                                    file_path: None, duration: None) -> bool:
        """
            Создание записи в таблицу статистики о неудачном выполнении запроса

        :param message:
        :param url:
        :param domen:
        :param file_name:
        :param file_path:
        :param duration:
        :return:
        """
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO request (url, domen, success, user_id, file_name,file_path, duration) VALUES (%s, %s, %s,%s, %s, %s, %s)",
                    (str(url), str(domen), False, str(message.chat.id), file_name, file_path, duration))
            except Exception:

                return False

            return True

    @info_log
    @exception
    def get_admin_chat_id(self) -> list:
        """
        Получаем ИД админ чата из БД
        :return:
        """

        with self.connection:
            self.cursor.execute('SELECT chat_id FROM admin_chat')
            chat_id = self.cursor.fetchall()
            return chat_id

    @info_log_message
    @exception
    def set_admin_chat_in_db(self, message: telebot.types.Message) -> bool:
        """
        Запись ИД админ чата в БД
        :param message:
        :return:
        """
        with self.connection:
            try:
                self.cursor.execute(
                    "INSERT INTO admin_chat (chat_id) VALUES (%s)",
                    (str(message.chat.id),))
            except Exception:

                return False

            return True
