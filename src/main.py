# -*- coding: utf-8 -*-

from vkbottle import Bot, Message

from src import messages, utils
from src.db import Users
from src.user import User

user = User()

API_TOKEN = "***REMOVED***"

bot = Bot(API_TOKEN)


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

@bot.on.message
def send_greetings(answer: Message):
    if not Users.contains(answer.chat_id):
        keyboard = utils.create_main_keyboard()
        answer(messages.hello, keyboard=keyboard.generate())

        # запоминает id пользователя; если его нет в базе, добавляется
        user.id = answer.chat_id


if __name__ == '__main__':
    bot.run_polling()
