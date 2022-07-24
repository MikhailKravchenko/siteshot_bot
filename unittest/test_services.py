# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal

from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import patch
import telebot

from ..src.services import Statistic, Shooter

message = {'content_type': 'text', 'id': 21715, 'message_id': 21715,
           'from_user': {'id': 178815386, 'is_bot': False, 'first_name': 'Mikhail', 'username': 'pirog',
                         'last_name': 'Kravchenko', 'language_code': 'ru', 'can_join_groups': None,
                         'can_read_all_group_messages': None, 'supports_inline_queries': None, 'is_premium': None,
                         'added_to_attachment_menu': None}, 'date': 1658660405,
           'chat': {'id': 178815386, 'type': 'private', 'title': None, 'username': 'pirog', 'first_name': 'Mikhail',
                    'last_name': 'Kravchenko', 'photo': None, 'bio': None, 'join_to_send_messages': None,
                    'join_by_request': None, 'has_private_forwards': None, 'description': None, 'invite_link': None,
                    'pinned_message': None, 'permissions': None, 'slow_mode_delay': None,
                    'message_auto_delete_time': None, 'has_protected_content': None, 'sticker_set_name': None,
                    'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None}, 'sender_chat': None,
           'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None,
           'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None,
           'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None,
           'author_signature': None, 'text': 'http://wikipedia.org', 'entities': '', 'audio': None, 'document': None,
           'sticker': None, 'video': None, 'video_note': None, 'voice': None, 'caption': None, 'location': None,
           'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 'left_chat_member': None,
           'new_chat_title': None, 'delete_chat_photo': None, 'group_chat_created': None,
           'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None,
           'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None,
           'connected_website': None, 'reply_markup': None, 'json': {
        'message_id': 21715,
        'from': {'id': 178815386, 'is_bot': False, 'first_name': 'Mikhail', 'last_name': 'Kravchenko',
                 'username': 'pirog',
                 'language_code': 'ru'},
        'chat': {'id': 178815386, 'first_name': 'Mikhail', 'last_name': 'Kravchenko', 'username': 'pirog',
                 'type': 'private'}, 'date': 1658660405, 'text': 'http://wikipedia.org',
        'entities': [{'offset': 0, 'length': 20, 'type': 'url'}]}}

call_back_message = {"id": "768006235155997284", "from": {"id": 178815386, "is_bot": False,
                                                          "first_name": "Mikhail",
                                                          "last_name": "Kravchenko",
                                                          "username": "pirog",
                                                          "language_code": "ru"},
                     "message": {"message_id": 13891, "data": "Like_2003",
                                 "from": {"id": 885507314,
                                          "is_bot": True, "first_name": "Miktest",
                                          "username": "mikhail13_bot"},
                                 "chat": {"id": 178815386,
                                          "first_name": "Mikhail",
                                          "last_name": "Kravchenko",
                                          "username": "pirog",
                                          "type": "private"},
                                 "date": 1639789217,
                                 "edit_date": 1639789218,
                                 "text": "Оцени мем от @pirog 👆",
                                 "entities": [{"offset": 13, "length": 6, "type": "mention"}],
                                 "reply_markup":
                                     {"inline_keyboard": [[{"text": "💚 0", "callback_data": "Like_2003"}],
                                                          [{"text": "😡 1", "callback_data": "Dislike_2003"}]]}},
                     "chat_instance": "4212169629247937782", "data": "Like_2003"}
expected_result_for_get_statistic_for_admin = """Количество запросов за все время: 64

Удачных запросов: 46

Неудачных запросов: 18

Топ URL: 
1. wikipedia.org количество запросов 34
2. yandex.ru количество запросов 9
3. www.vprok.ru количество запросов 7
4. wifgdsfbdfndfnkipedia.org количество запросов 3
5. wikipsdgsdfhedia.org количество запросов 2
6. wikidfhdfgpedia.org количество запросов 2
7. www.youtube.com количество запросов 1
8. piccolo-orm.com количество запросов 1
9. wikidertyuytrtyuytrtyuytyujytyugfghgfghjhgfhdfgpedia.org.hgfghjk.yu количество запросов 1
10. kudrovo.hh.ru количество запросов 1


Топ пользователей:
1. ID: 178815386, username: pirog, first_name: Mikhail, количество запросов 59
2. ID: 3463547, username: отсутствует, first_name: отсутствует, количество запросов 3
3. ID: 1, username: отсутствует, first_name: отсутствует, количество запросов 2

Среднее время выполнения запроса: 5.9130 сек."""


class Launcher:
    def __init__(self):
        pass

    async def launch(self):
        return Browser()


class Browser:
    def __init__(self):
        pass

    async def newPage(self):
        return True

    async def setViewport(self, option):
        return True

    async def goto(self, url):
        return True


class Chat:
    def __init__(self, chat):
        self.id = chat['id']


class Message:
    def __init__(self, message_id, from_user, date, chat, content_type):
        self.content_type: str = content_type
        self.id: int = message_id  # Lets fix the telegram usability ####up with ID in Message :)
        self.message_id: int = message_id
        self.from_user = from_user
        self.date: int = date
        self.chat = Chat(chat)


class Postgers():
    def __init__(self):
        pass

    def get_statistic(self):
        count_requests = [(64,)]
        count_success_requests = [(46,)]
        count_not_success_requests = [(18,)]
        top_domen = [('wikipedia.org', 34), ('yandex.ru', 9), ('www.vprok.ru', 7), ('wifgdsfbdfndfnkipedia.org', 3),
                     ('wikipsdgsdfhedia.org', 2), ('wikidfhdfgpedia.org', 2), ('www.youtube.com', 1),
                     ('piccolo-orm.com', 1), ('wikidertyuytrtyuytrtyuytyujytyugfghgfghjhgfhdfgpedia.org.hgfghjk.yu', 1),
                     ('kudrovo.hh.ru', 1)]
        top_users = [(178815386, 'pirog', 'Mikhail', 59), (3463547, None, None, 3), (1, None, None, 2)]
        average_duration = [(Decimal('5.9130434782608696'),)]
        return count_requests, count_success_requests, count_not_success_requests, top_domen, top_users, average_duration


class TestStatisticClass(TestCase):

    def test_get_statistic_for_admin(self):
        self.message = telebot.types.Message.de_json(message)
        messages = telebot.types.Message(message['id'], message['from_user'], message['date'], message['chat'],
                                         message['content_type'], {'name': "gg"}, 'options')
        print(messages)
        db_worker = Postgers()
        get_statistic = Statistic(db_worker)
        result = get_statistic.get_statistic_for_admin()

        self.assertEqual(result, expected_result_for_get_statistic_for_admin)


class TestShooterClass(IsolatedAsyncioTestCase):

    @patch("pyppeteer.launch")
    async def test_get_screen_and_save_page(self, mock_pyppeteer_launch):
        messages = Message(message['id'], message['from_user'], message['date'], message['chat'],
                           message['content_type'])
        launch = Launcher()
        mock_pyppeteer_launch.return_value = await launch.launch()
        url = 'http://wikipedia.org'
        domen = 'wikipedia.org'
        shooter = Shooter()
        filename, file_path, title, duration = await shooter.get_screen_and_save_page(messages, url, domen)

        self.assertEqual(filename, '2022_07_24_11_00_05_178815386_wikipedia_org.png')
        self.assertEqual(file_path, 'storage/2022_07_24_11_00_05_178815386_wikipedia_org.png')
        self.assertEqual(title, None)