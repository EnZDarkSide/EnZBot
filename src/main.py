# -*- coding: utf-8 -*-

from vkbottle import Bot, Message

from src import messages, utils
from src.db import Users
from src.utils import trolleys_menu, general_menu

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


@bot.on.message(text=['Начать'])
async def send_greetings(answer: Message):
    await bot.branch.exit(answer.peer_id)

    user = await bot.api.users.get(user_ids=[answer.from_id])

    await bot.api.messages.send(
        user_id=answer.from_id,
        keyboard=general_menu(),
        message=messages.send_greetings(user[0].sex),
        random_id=bot.extension.random_id()
    )

    if not Users.contains(answer.from_id):
        Users.add(answer.from_id, f'{user[0].first_name} {user[0].last_name}')


@bot.on.message(text=['Меню', 'Главное меню', '?'])
async def send_menu(answer: Message):
    await answer(message='Призываем меню!', keyboard=utils.general_menu())


@bot.on.message(text=['Добавить себя'])
async def add_user(answer: Message):
    if not Users.add(answer.peer_id):
        await answer("Возникла ошибка. Попробуй позже", keyboard=general_menu())
        return

    await answer("Готово")


@bot.on.message(text=['Указать адрес'])
async def updating_address_start(answer: Message):
    await answer("Укажите свой адрес")
    await move_to_branch(answer.peer_id, "updating_address")


@bot.branch.simple_branch("updating_address")
async def update_address(answer: Message):
    if str.lower(answer.text) not in ['назад', 'выйти', 'главное меню', 'меню']:
        if not Users.update_address(answer.from_id, answer.text):
            await answer(messages.error, keyboard=general_menu())
            return

    await bot.branch.exit(answer.peer_id)
    await answer("Готово! Данные занесены в базу", keyboard=general_menu())


@bot.on.message(text=['Где трамваи?'])
async def show_trolleys(answer: Message):
    await answer(messages.trolleys_available, keyboard=trolleys_menu())
    await move_to_branch(answer.peer_id, "trolleys_menu")


@bot.branch.simple_branch("trolleys_menu")
async def show_trolleys(answer: Message):
    if 'обновить данные' in str.lower(answer.text):
        pass
    elif 'главное меню' in str.lower(answer.text):
        await bot.branch.exit(answer.peer_id)
        await send_menu(answer)
        return

    await answer(messages.trolleys_available, keyboard=trolleys_menu())


async def move_to_branch(peer_id: int, branch_name: str):
    await bot.branch.exit(peer_id)
    await bot.branch.add(peer_id, branch_name)

if __name__ == '__main__':
    bot.run_polling()
