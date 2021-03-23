# -*- coding: utf-8 -*-
import os

from tortoise import Tortoise
from vkbottle import Message
from vkbottle.branch import Branch

from src import messages, utils
from src.bot import bot
from src.database.enitities import DBGroups
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
    if not DBGroups.get(answer.from_id):
        await answer('Чтобы продолжить, вам нужно вписать группу для расписания')
        return Branch('groups_update')

    await answer(message=messages.resp_show_menu, keyboard=utils.general_keyboard())


@bot.on.message()
async def rand_message(answer: Message):
    if not DBGroups.get(answer.from_id):
        await answer('Чтобы продолжить, вам нужно вписать группу для расписания')
        return Branch('groups_update')

    await answer("Вызываем меню", keyboard=general_keyboard())


async def init_db():
    await Tortoise.init(
        db_url=os.environ['CLEARDB_DATABASE_URL_WOREC'], modules={"models": ["src.database.models"]}
    )
    await Tortoise.generate_schemas(safe=True)

if __name__ == '__main__':
    bot.run_polling(on_startup=init_db)
