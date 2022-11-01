# -*- coding: utf-8 -*-
import asyncio
import json
import ssl
import urllib

import telebot
from aiohttp import web
from telebot import types
from telebot.async_telebot import AsyncTeleBot

from abstract import AbstractCore
from decor import exception, info_log_message_async, info_log_message_async_callback
from env import (
    WEBHOOK_LISTEN,
    WEBHOOK_PORT,
    WEBHOOK_SSL_CERT,
    WEBHOOK_SSL_PRIV,
    WEBHOOK_URL_BASE,
    WEBHOOK_URL_PATH,
    token,
    webhook,
)
from PostgreSQL import PostgreSQL
from services import Shooter, Statistic, ValidateUrl

app = web.Application()


class Core(AbstractCore):
    """ Bot core. Starts listening for new messages.
         Responsible for calling methods on certain commands from the chat and for pressing buttons
        """

    def __init__(self) -> None:
        self.bot = AsyncTeleBot(token)

        @self.bot.message_handler(commands=['start'])
        @exception
        async def _command_start(message: telebot.types.Message or telebot.types.CallbackQuery) -> None:
            """Fires when a command is entered /start"""
            await self.process_comand_start(message)

        @self.bot.message_handler(commands=['admin'])
        @exception
        async def _command_admin(message: telebot.types.Message or telebot.types.CallbackQuery) -> None:
            """Fires when a command is entered /admin"""

            await self.process_comand_admin(message)

        @self.bot.message_handler(commands=['setadminchat'])
        @exception
        async def _command_set_admin_chat(message: telebot.types.Message or telebot.types.CallbackQuery) -> None:
            """Fires when a command is entered /setadminchat"""

            await self.process_set_admin_chat(message)

        @self.bot.message_handler(commands=['statistic'])
        @exception
        async def _command_statistic(message: telebot.types.Message or telebot.types.CallbackQuery) -> None:
            """Fires when a command is entered /statistic"""

            await self.process_get_statistic(message)

        @self.bot.message_handler(func=lambda message: True, content_types=['text'])
        @exception
        async def _check_text_and_get_screen(message: telebot.types.Message) -> None:
            """Fires when any text message is received"""
            await self.process_check_text_and_get_screen(message)

        @self.bot.callback_query_handler(func=lambda c: True)
        @exception
        @info_log_message_async_callback
        async def process_callback_btn(callback_query: types.CallbackQuery, info: dict) -> None:
            """Fires when the Details button is clicked.
                 Requests the necessary data about the site with the free API of one of the WHOIS services
                 and gives the received information to the user
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
                                                      f'Continent: {continent}\n'
                                                      f'Country: {country}\n'
                                                      f'City: {city}\n \n'
                                                      f'Provider: {isp}\n'
                                                      f'Org: {org}\n',
                                                 show_alert=True)

    @info_log_message_async
    @exception
    async def process_comand_start(self, message: telebot.types.Message) -> None:
        """/start command method
             Checks whether there is such a user in the database, if not, then adds, if there is, then updates information about him.
             Sends a welcome message
            """
        db_worker = PostgreSQL()
        if not db_worker.set_user_info_in_db(message):
            db_worker.update_user_in_db(message)

        await self.bot.send_message(message.chat.id,
                                    '👋🏻 Hello! My name is Jpeger. I am a Web Screenshot Bot.'
                                    'To get a screenshot - send the URL of the site. For example, wikipedia.org \n'
                                    '• With the help of a bot you can check suspicious links. '
                                    '(IP loggers, phishing websites, screamers, etc.)\n'
                                    '• You can also add me to your chats so I can check the links, '
                                    'submitted by users')

    @info_log_message_async
    @exception
    async def process_comand_admin(self, message: telebot.types.Message) -> None:
        """

        :param message: telebot.types.Message
        :return:
        /admin command method
         If there is no admin chat, then he proposes to assign
         If there is and the command is sent in the admin chat, then it gives help on the admin commands
         If there is and the chat is not Alminsky, it simply ignores


        """
        db_worker = PostgreSQL()
        admin_chat_id = db_worker.get_admin_chat_id()
        if not admin_chat_id:
            await self.bot.send_message(message.chat.id, "There is no admin chat yet.\n"
                                                         "To make this chat the bot admin's chat,"
                                                         " enter command /setadminchat")
            return
        if admin_chat_id[0][0] == message.chat.id:
            await self.bot.send_message(message.chat.id,
                                        '/statistic - Get bot statistics \n'
                                        )

    @info_log_message_async
    @exception
    async def process_set_admin_chat(self, message: telebot.types.Message) -> None:
        """
        Designates the current chat as the admin chat if it is not assigned
        """
        db_worker = PostgreSQL()

        if db_worker.set_admin_chat_in_db(message):

            await self.bot.send_message(message.chat.id,
                                        'Now this chat is admin, all admin commands are available \n'
                                        'To list commands /admin')
        else:
            await self.bot.send_message(message.chat.id,
                                        'This bot already has an admin chat assigned')

    @info_log_message_async
    @exception
    async def process_get_statistic(self, message: telebot.types.Message) -> None:
        """

        :param message: telebot.types.Message
        :return:

        Requests statistics and gives it to the user
        """
        db_worker = PostgreSQL()
        try:
            statistic = Statistic(db_worker)
            get_statistic = statistic.get_statistic_for_admin()
            await self.bot.send_message(message.chat.id, get_statistic)
        except TypeError:
            await self.bot.send_message(message.chat.id, 'Statistics is empty')

    @info_log_message_async
    @exception
    async def process_check_text_and_get_screen(self, message: telebot.types.Message) -> None:
        """

        :param message: telebot.types.Message
        :return:
        Checks for URL validity (with django opensource tweaked slightly)
         Sends the user information that the request has been sent.
         After receiving the image, sends it to the user, attaching information and a WHOIS button
         On error, sends information that an error has occurred (for example, timeout 30000ms)
         If the text is not a URL then ignore the message
        """
        # Updating user information
        db_worker = PostgreSQL()
        db_worker.update_user_in_db(message)

        validation_url = ValidateUrl(message.text)
        # URL validation check
        if validation_url.validate():
            # Getting a domain from a URL
            domen = validation_url.parse_url()
            # Informing the user that the request has been sent
            send_message = await self.bot.send_message(message.chat.id,
                                                       u'\U000026A1' + '️_Request sent to site..._',
                                                       reply_to_message_id=message.message_id, parse_mode="Markdown")
            shooter = Shooter()
            # Getting Screen and related information: file name, path, page name, execution time
            filename, file_path, title, duration = await shooter.get_screen_and_save_page(message, validation_url.url,
                                                                                          domen)
            # Checking if there was an error while executing the request
            if shooter._error:
                # Submitting error information
                with open('animation.gif.mp4', 'rb') as file:
                    await self.bot.send_video(message.chat.id, file)
                    await self.bot.send_message(message.chat.id, '*Error executing request*',
                                                parse_mode="Markdown")
                    await self.bot.delete_message(message.chat.id, message_id=send_message.message_id)
                    # Adding info to the database for statistics
                    db_worker.set_statistic_succses_false(message, validation_url.url, domen, filename, file_path,
                                                          duration)

                    return
            # If there are no errors, send the screen info and the button
            with open(file_path, 'rb') as file:
                markup = types.InlineKeyboardMarkup(row_width=1)
                button = types.InlineKeyboardButton(u'\U0001F52C' + ' Details', callback_data=str(domen))
                markup.add(button)
                await self.bot.send_photo(message.chat.id, file, caption=f'{title} \n'
                                                                         f'\n'
                                                                         f'<b>Web site:</b> {validation_url.url} \n'
                                                                         f'\n'
                                                                         f'<b>Time of processing</b>: {int(duration)} секунд',
                                          reply_markup=markup,
                                          parse_mode='HTML')

            await self.bot.delete_message(message.chat.id, message_id=send_message.message_id)
            # Adding info to the database for statistics
            db_worker.set_statistic_succses_true(message, validation_url.url, domen, filename, file_path, duration)

    @info_log_message_async
    @exception
    async def get_data(self, request: object) -> web.Response:
        """

        :param request:
        :return:
        Updates information about new messages for the bot
        """
        if request.match_info.get('token') == self.bot.token:
            request_body_dict = await request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            await self.bot.process_new_updates([update])
            return web.Response()
        else:
            return web.Response(status=403)

    @exception
    async def run(self) -> None:
        """

        :return:
        Running bot polling
        """
        await self.bot.remove_webhook()

        await self.bot.polling(non_stop=True, skip_pending=True, timeout=40, request_timeout=40)  # to skip updates

    @exception
    def run_webhook(self) -> None:
        """
        Running bot webhooks
        """
        with open(WEBHOOK_SSL_CERT, 'r') as ssl_cert:
            self.bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                                 certificate=ssl_cert)

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
# Depending on the settings, select the type of connection
if webhook is True:
    core = Core()
    core.run_webhook()

else:
    if __name__ == '__main__':
        core = Core()
        asyncio.run(core.run())
