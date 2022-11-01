# -*- coding: utf-8 -*-
import asyncio
import json
import urllib
import ssl
import telebot


from abstract import AbstractCore
from loging import logging
from services import Shooter, ValidateUrl, Statistic
from env import *
from aiohttp import web
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from decor import exception, info_log_message_async, info_log_message_async_callback

from PostgreSQL import PostgreSQL

app = web.Application()


class Core(AbstractCore):
    """ Ядро бота. Запускает прослушивание новых сообщений.
        Отвечает за вызов методов при определенных командах из чата и за нажатие кнопок
        """

    def __init__(self):
        self.bot = AsyncTeleBot(token)

        @self.bot.message_handler(commands=['start'])
        @exception
        async def _command_start(message: telebot.types.Message or telebot.types.CallbackQuery):
            """Срабатывает при вводе команды /start"""
            await self.process_comand_start(message)

        @self.bot.message_handler(commands=['admin'])
        @exception
        async def _command_admin(message: telebot.types.Message or telebot.types.CallbackQuery):
            """Срабатывает при вводе команды /admin"""

            await self.process_comand_admin(message)

        @self.bot.message_handler(commands=['setadminchat'])
        @exception
        async def _command_set_admin_chat(message: telebot.types.Message or telebot.types.CallbackQuery):
            """Срабатывает при вводе команды /setadminchat"""

            await self.process_set_admin_chat(message)

        @self.bot.message_handler(commands=['statistic'])
        @exception
        async def _command_statistic(message: telebot.types.Message or telebot.types.CallbackQuery):
            """Срабатывает при вводе команды /statistic"""

            await self.process_get_statistic(message)

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        @exception
        async def _check_text_and_get_screen(message: telebot.types.Message):
            """Срабатывает при получении любых текстовых сообщений"""
            await self.process_check_text_and_get_screen(message)

        @self.bot.callback_query_handler(func=lambda c: True)
        @exception
        @info_log_message_async_callback
        async def process_callback_btn(callback_query: types.CallbackQuery):
            """Срабатывает при нажатии на кнопку Подробнее.
                Запрашивает необходимые данные о сайте с free API одного из WHOIS сервисов
                и выдает полученную информацию пользователю
            """

            callback_data = callback_query.data
            url_ip = f'http://ip-api.com/json/{callback_data}?fields=query,continent,country,city,isp,org'
            getinfo = urllib.request.urlopen(url_ip)
            data = json.load(getinfo)
            ip = data['query']
            continent = data['continent']
            country = data['country']
            city = data['city']
            isp = data['isp']
            org = data['org']

            await self.bot.answer_callback_query(callback_query.id,
                                                 text=f'IP: {ip}\n \n'
                                                      f'Континент: {continent}\n'
                                                      f'Страна: {country}\n'
                                                      f'Город: {city}\n \n'
                                                      f'Провайдер: {isp}\n'
                                                      f'Организация: {org}\n',
                                                 show_alert=True)

    @info_log_message_async
    @exception
    async def process_comand_start(self, message: telebot.types.Message):
        """Метод команды /start
            Проверяет есть ли такой пользователь в БД, если нет то добавляет, если есть то ообновляет информацию о нем.
            Посылает приветственное инф сообщение
            """
        db_worker = PostgreSQL()
        if not db_worker.set_user_info_in_db(message):
            db_worker.update_user_in_db(message)

        await self.bot.send_message(message.chat.id,
                                    f'👋🏻 Привет! Меня зовут Jpeger. Я - Бот для создания веб-скриншотов.'
                                    f'Чтобы получить скриншот - отправьте URL адрес сайта. Например, wikipedia.org \n'
                                    f'• С помощью бота вы можете проверять подозрительные ссылки. '
                                    f'(Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)\n'
                                    f'• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, '
                                    f'которые отправляют пользователи')

    @info_log_message_async
    @exception
    async def process_comand_admin(self, message: telebot.types.Message):
        """

        :param message: telebot.types.Message
        :return:
        Метод команды /admin
        Если админ чата нет, то прелагает назначить
        Если есть и команда передана в админ чате, то выдает справку по командам админа
        Если есть и чат не алминский просто игнорирует


        """
        db_worker = PostgreSQL()
        admin_chat_id = db_worker.get_admin_chat_id()
        if not admin_chat_id:
            await self.bot.send_message(message.chat.id, f'Административного чата еще нет.\n'
                                                         f'Чтобы сделать этот чат чатом администратора бота,'
                                                         f' введите команду /setadminchat')
            return
        if admin_chat_id[0][0] == message.chat.id:
            await self.bot.send_message(message.chat.id,
                                        f'/statistic - Получить статистику работы бота \n'
                                        )

    @info_log_message_async
    @exception
    async def process_set_admin_chat(self, message: telebot.types.Message):
        """
        Назначает текущий чат чатом администратора, если он не назначен
        """
        db_worker = PostgreSQL()

        if db_worker.set_admin_chat_in_db(message):

            await self.bot.send_message(message.chat.id,
                                        f'Теперь этот чат административный, вам доступны все команды администратора \n'
                                        f'Для вывода списка комманд /admin')
        else:
            await self.bot.send_message(message.chat.id,
                                        f'У этого бота уже назначен административный чат')

    @info_log_message_async
    @exception
    async def process_get_statistic(self, message: telebot.types.Message):
        """

        :param message: telebot.types.Message
        :return:

        Запрашивает статистику и предает ее пользователю
        """
        db_worker = PostgreSQL()
        try:
            statistic = Statistic(db_worker)
            get_statistic = statistic.get_statistic_for_admin()
            await self.bot.send_message(message.chat.id, get_statistic)
        except TypeError:
            await self.bot.send_message(message.chat.id, 'Статистика пуста')
    @info_log_message_async
    @exception
    async def process_check_text_and_get_screen(self, message: telebot.types.Message):
        """

        :param message: telebot.types.Message
        :return:
        Праверяет на валидность URL (с помощью django opensource слегка доработанного)
        Отправляет пользователю информацию что запрос отправлен
        После получения изображения отправляет его пользователю, прикрепляя информацию и кнопку WHOIS
        При ошибке отправляет информацию что произошла ошибка (к примеру timeout 30000ms)
        Если тескт не является URL то игнорирует сообщение
        """
        # Обновление информации о поьзователе
        db_worker = PostgreSQL()
        db_worker.update_user_in_db(message)

        validation_url = ValidateUrl(message.text)
        # Проверка на валидность URL
        if validation_url.validate():
            # Получение домена из URL
            domen = validation_url.parse_url()
            # Информирование пользователя что запрос отправлен
            send_message = await self.bot.send_message(message.chat.id,
                                                       u'\U000026A1' + '️_Запрос отправлен на сайт..._',
                                                       reply_to_message_id=message.message_id, parse_mode="Markdown")
            shooter = Shooter()
            # Получение Скрина и сопутсвуещей информации: имя файла, путь, Название страницы, время выполнения
            filename, file_path, title, duration = await shooter.get_screen_and_save_page(message, validation_url.url,
                                                                                          domen)
            # Проверка была ли ошибка во время выполнения запроса
            if shooter._error:
                # ОТправляем информацию об ошибке
                img = open('animation.gif.mp4', 'rb')
                await self.bot.send_video(message.chat.id, img)
                img.close()
                await self.bot.send_message(message.chat.id, f'*Ошибка выполнения запроса*',
                                            parse_mode="Markdown")
                await self.bot.delete_message(message.chat.id, message_id=send_message.message_id)
                # Добавляем инфу в бд для статистики
                db_worker.set_statistic_succses_false(message, validation_url.url, domen, filename, file_path, duration)

                return
            # Если ошибок нет, отправляем скрин инфу и кнопу
            with open(file_path, 'rb') as file:
                markup = types.InlineKeyboardMarkup(row_width=1)
                button = types.InlineKeyboardButton(u'\U0001F52C' + ' Подробнее', callback_data=str(domen))
                markup.add(button)
                await self.bot.send_photo(message.chat.id, file, caption=f'{title} \n'
                                                                         f'\n'
                                                                         f'<b>Веб-сайт:</b> {validation_url.url} \n'
                                                                         f'\n'
                                                                         f'<b>Время обработки</b>: {int(duration)} секунд',
                                          reply_markup=markup,
                                          parse_mode='HTML')

            await self.bot.delete_message(message.chat.id, message_id=send_message.message_id)
            # Добавляем инфу в бд для статистики
            db_worker.set_statistic_succses_true(message, validation_url.url, domen, filename, file_path, duration)

    @info_log_message_async
    @exception
    async def get_data(self, request):
        """

        :param request:
        :return:
        Обновления информации о новых сообщениях для бота
        """
        if request.match_info.get('token') == self.bot.token:
            request_body_dict = await request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            await self.bot.process_new_updates([update])
            return web.Response()
        else:
            return web.Response(status=403)

    @exception
    async def run(self):
        """

        :return:
        Запуск бота polling
        """
        await self.bot.remove_webhook()

        await self.bot.polling(non_stop=True, skip_pending=True, timeout=40, request_timeout=40)  # to skip updates

    @exception
    def run_webhook(self):
        """
        Запуск бота webhooks
        """
        self.bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                             certificate=open(WEBHOOK_SSL_CERT, 'r'))

        # Build ssl context
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

        # Start aiohttp server
        web.run_app(
            app,
            host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            ssl_context=context,
        )


app.router.add_post('/{token}/', Core().get_data)
# В зависимости от настроек выбираем тип подключения
if webhook is True:
    core = Core()
    core.run_webhook()

else:
    if __name__ == '__main__':
        core = Core()
        asyncio.run(core.run())
