# -*- coding: utf-8 -*-
import asyncio

import telebot
import ssl

from siteshot_bot.abstract import AbstractCore
from loging import logging
from siteshot_bot.services import Shooter, ValidateUrl

from siteshot_bot import env
from aiohttp import web
from datetime import datetime
from telebot.async_telebot import AsyncTeleBot

app = web.Application()


# Process webhook calls
class Core(AbstractCore):
    def __init__(self):
        self.bot = AsyncTeleBot(env.token)

        @self.bot.message_handler(commands=['start'])
        async def _command_start(message: telebot.types.Message or telebot.types.CallbackQuery):
            await self.process_comand_start(message)

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        async def _check_text_and_get_screen(message):
            await self.process_check_text_and_get_screen(message)

    async def process_comand_start(self, message):
        await self.bot.send_message(message.chat.id, 'Информация справочная')

    async def process_check_text_and_get_screen(self, message):

        try:
            if message.chat.first_name:
                first_name = message.chat.first_name
            else:
                first_name = message.from_user.first_name
            d = {'facility': 'answer', 'user.id': str(message.from_user.id), 'first_name': str(first_name),
                 'text': str(message.text),
                 'time_answer':
                     str(datetime.utcfromtimestamp(message.date).strftime('%Y-%m-%d %H:%M:%S'))}
            logging.info('User Message', extra=d)

        except:
            pass
        validation_url = ValidateUrl(message.text)

        if validation_url.validate():
            domen = validation_url.parse_url()[0]
            send_message = await self.bot.send_message(message.chat.id, "Ваш запрос принят")
            shooter = Shooter(message)

            await shooter.get_screen_page(validation_url.url)

            await shooter.save_screen(message, validation_url.url, domen)

            await self.bot.edit_message_text('text',
                                             message.chat.id,
                                             message_id=send_message.message_id)

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
        self.bot.set_webhook(url=env.WEBHOOK_URL_BASE + env.WEBHOOK_URL_PATH,
                             certificate=open(env.WEBHOOK_SSL_CERT, 'r'))

        # Build ssl context
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain(env.WEBHOOK_SSL_CERT, env.WEBHOOK_SSL_PRIV)

        # Start aiohttp server
        web.run_app(
            app,
            host=env.WEBHOOK_LISTEN,
            port=env.WEBHOOK_PORT,
            ssl_context=context,
        )


app.router.add_post('/{token}/', Core().get_data)

if env.webhook is True:
    core = Core()
    core.run_webhook()

else:
    if __name__ == '__main__':
        core = Core()
        asyncio.run(core.run())
