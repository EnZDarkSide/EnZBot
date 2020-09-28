# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from src.db import Users
from src.user import User

user = User()

API_TOKEN = "***REMOVED***"
API_VERSION = "5.131"

vk_session = vk_api.VkApi(token=API_TOKEN, api_version=API_VERSION)
api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id='184750146')


# добавление пользователя в базу данных
# приветствие
# вывод меню
# добавление нескольких групп
# узнавание рейтинга
# узнавание домашки
# узнавание новой домашки (возможно)
# трамваи
# метро
# настройки
# кто хочет сходить в магазин?
# объявления от пользователей(?)

def send_greetings(event):
    api.messages.send(user_id=event.message.from_id,
                      message="Привет, добро пожаловать! Обращайся ко мне, если нужно узнать расписание в "
                              "твоей группе, расписание трамваев и метро, твой рейтинг на портале или дать "
                              "объявление, которое увидят все пользователи",
                      keyboard=create_general_keyboard(),
                      random_id=get_random_id())


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if not Users.contains(event.message.from_id):
                send_greetings(event)

            # запоминает id пользователя; если его нет в базе, добавляется
            user.id = event.message.from_id


def create_general_keyboard():
    _keyboard = VkKeyboard(one_time=True)

    _keyboard.add_button('Добавить группу', color=VkKeyboardColor.SECONDARY)
    _keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)
    _keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)

    _keyboard.add_line()  # Переход на вторую строку
    _keyboard.add_location_button()

    return _keyboard.get_keyboard()


if __name__ == '__main__':
    main()
