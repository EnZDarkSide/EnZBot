# -*- coding: utf-8 -*-
from vkbottle import Message

from src import messages, utils
from src.bot import bot
from src.utils import general_keyboard

# приветствие
# добавление нескольких групп
# узнавание рейтинга
# узнавание домашки
# узнавание новой домашки (возможно)
# трамваи
# метро
# настройки


@bot.on.message(text=['Меню', 'Главное меню', '?'])
async def send_menu(answer: Message):
    await answer(message=messages.resp_show_menu, keyboard=utils.general_keyboard())


@bot.on.message()
async def rand_message(answer: Message):
    await answer("Вызываем меню", keyboard=general_keyboard())


if __name__ == '__main__':
    bot.run_polling()
