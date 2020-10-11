# -*- coding: utf-8 -*-

from vkbottle import Bot, Message, api

from vkbottle.types import GroupJoin, MessageAllow

from src import messages, utils
from src.db import Users

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


def general_menu():
    return utils.create_keyboard([{"text": "Добавить группу"}, {"text": 'Указать адрес'}], [{"text": "Где трамваи?"}])


@bot.on.event.message_allow()
async def send_greetings(event: MessageAllow):
    user = await bot.api.users.get(user_ids=[event.user_id])

    await bot.api.messages.send(
        user_id=event.user_id,
        keyboard=general_menu(),
        message=messages.send_greetings(user[0].sex),
        random_id=bot.extension.random_id()
    )

    if not Users.contains(event.user_id):
        Users.add(event.user_id, f'{user[0].first_name} {user[0].last_name}')


@bot.on.message(text=['Меню', 'Главное меню'])
async def send_menu(answer: Message):
    await answer(message='Призываем меню!', keyboard=general_menu())


@bot.on.message(text=['Добавить себя'])
async def add_user(answer: Message):
    if not Users.add(answer.from_user):
        await answer("Возникла ошибка. Попробуй позже")
        return

    await answer("Готово")


@bot.on.message(text=['Указать адрес'])
async def updating_address_start(answer: Message):
    await answer("Укажите свой адрес")
    await bot.branch.add(answer.peer_id, "updating_address")


@bot.branch.simple_branch("updating_address")
async def update_address(answer: Message):
    if not Users.update_address(answer.from_id, answer.text):
        await answer(messages.error, general_menu())

    await answer("Готово! Данные занесены в базу", general_menu())

    await bot.branch.exit(answer.peer_id)


@bot.on.message(text=['Где трамваи?'])
async def show_trolleys(answer: Message):
    keyboard = utils.create_keyboard([{"text": 'Обновить данные'}, {"text": 'Указать адрес'}],
                                     [{"text": 'Главное меню', "color": "secondary"}])
    await answer(messages.trolleys, keyboard=keyboard)


@bot.on.message(text=['Обновить данные'])
async def show_trolleys(answer: Message):
    keyboard = utils.create_keyboard([{"text": 'Обновить данные'}, {"text": 'Указать адрес'}],
                                     [{"text": 'Главное меню', "color": "secondary"}])
    await answer(messages.trolleys, keyboard=keyboard)


if __name__ == '__main__':
    bot.run_polling()
