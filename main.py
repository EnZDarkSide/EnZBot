# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import pymysql

API_TOKEN = "***REMOVED***"
API_VERSION = "5.131"

vk_session = vk_api.VkApi(token=API_TOKEN, api_version=API_VERSION)
api = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id='184750146')

con = pymysql.connect('localhost', 'root',
                      '', 'enzbotdb')
cur = con.cursor()


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


def get_user(user_id):
    cur.execute(str.format('SELECT * FROM users WHERE UserId={0}', user_id))
    return cur.fetchone()


def add_user(user_id):
    user = api.users.get(user_ids=user_id)[0]
    if user is None:
        return
    full_name = user['first_name'] + " " + user['last_name']
    command = str.format("INSERT INTO users (UserId, FullName) VALUES ('{0}','{1}')",
                           user_id, full_name)
    cur.execute(command)


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if get_user(event.message.from_id) is None:
                send_greetings(event)
                add_user(event.message.from_id)

            # проверить на наличие пользователя в базе данных. Занести при нажатии старт.


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
