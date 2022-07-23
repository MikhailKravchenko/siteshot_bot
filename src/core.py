# -*- coding: utf-8 -*-
import asyncio
import json
import urllib
import telebot
import ssl

from abstract import AbstractCore
from loging import logging
from services import Shooter, ValidateUrl
from env import *
from aiohttp import web
from datetime import datetime
from telebot.async_telebot import AsyncTeleBot
from telebot import types

from PostgreSQL import PostgreSQL

app = web.Application()


class Core(AbstractCore):
    def __init__(self):
        self.bot = AsyncTeleBot(token)

        @self.bot.message_handler(commands=['start'])
        async def _command_start(message: telebot.types.Message or telebot.types.CallbackQuery):
            await self.process_comand_start(message)

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        async def _check_text_and_get_screen(message):
            await self.process_check_text_and_get_screen(message)

        @self.bot.callback_query_handler(func=lambda c: True)
        async def process_callback_btn_detailed(callback_query: types.CallbackQuery):
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

    async def process_comand_start(self, message):
        db_worker = PostgreSQL()
        if not db_worker.set_user_info_in_db(message):
            db_worker.update_user_in_db(message)

        await self.bot.send_message(message.chat.id,
                                    f'👋🏻 Привет! Меня зовут Jpeger. Я - Бот для создания веб-скриншотов.Чтобы получить скриншот - отправьте URL адрес сайта. Например, wikipedia.org \n'
                                    f'• С помощью бота вы можете проверять подозрительные ссылки. (Айпилоггеры, фишинговые веб-сайты, скримеры и т.п)\n'
                                    f'• Вы также можете добавить меня в свои чаты, и я смогу проверять ссылки, которые отправляют пользователи')

    async def process_check_text_and_get_screen(self, message):

        db_worker = PostgreSQL()
        db_worker.update_user_in_db(message)

        if message.chat.first_name:
            first_name = message.chat.first_name
        else:
            first_name = message.from_user.first_name
        d = {'facility': 'answer', 'user.id': str(message.from_user.id), 'first_name': str(first_name),
             'text': str(message.text),
             'time_answer':
                 str(datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}
        logging.info('User Message', extra=d)


        validation_url = ValidateUrl(message.text)

        if validation_url.validate():

            domen = validation_url.parse_url()
            send_message = await self.bot.send_message(message.chat.id,
                                                       u'\U000026A1' + '️_Запрос отправлен на сайт..._',
                                                       reply_to_message_id=message.message_id, parse_mode="Markdown")
            shooter = Shooter(message)

            filename, file_path, title, duration = await shooter.get_screen_and_save_page(message, validation_url.url, domen)
            if shooter._error:
                img = open('animation.gif.mp4', 'rb')
                await self.bot.send_video(message.chat.id, img)
                img.close()
                await self.bot.send_message(message.chat.id, f'*Ошибка выполнения запроса*',
                                            parse_mode="Markdown")
                await self.bot.delete_message(message.chat.id, message_id=send_message.message_id)
                db_worker.set_statistic_succses_false(message, validation_url.url, domen, filename, file_path, duration)

                return

            with open(file_path, 'rb') as file:
                markup = types.InlineKeyboardMarkup(row_width=1)
                button = types.InlineKeyboardButton(u'\U0001F52C' + ' Подробнее', callback_data=str(domen))
                markup.add(button)
                await self.bot.send_photo(message.chat.id, file, caption=f'{title} \n'
                                                                         f'\n'
                                                                         f'*Веб-сайт*: {validation_url.url} \n'
                                                                         f'\n'
                                                                         f'*Время обработки*: {int(duration)} секунд',
                                          reply_markup=markup,
                                          parse_mode="Markdown")

            await self.bot.delete_message(message.chat.id, message_id=send_message.message_id)
            db_worker.set_statistic_succses_true(message, validation_url.url, domen, filename, file_path, duration)
        else:
            await self.bot.send_message(message.chat.id, "Не верный ULR")

    async def get_data(self, request):
        if request.match_info.get('token') == self.bot.token:
            request_body_dict = await request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            await self.bot.process_new_updates([update])
            return web.Response()
        else:
            return web.Response(status=403)

    async def run(self):
        await self.bot.remove_webhook()

        await self.bot.polling(non_stop=True, skip_pending=True)  # to skip updates

    def run_webhook(self):
        # Set webhook run_webhooks
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

if webhook is True:
    core = Core()
    core.run_webhook()

else:
    if __name__ == '__main__':
        core = Core()
        asyncio.run(core.run())
