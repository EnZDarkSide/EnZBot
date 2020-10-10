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


@bot.on.event.message_allow()
@bot.on.event.group_join()
async def send_greetings(event: MessageAllow or GroupJoin):
    if not Users.contains(event.user_id):
        await bot.api.messages.send(
            peer_id=event.user_id,
            message=messages.hello,
            keyboard=utils.create_keyboard('Добавить группу', 'Указать адрес', 'Где трамваи?'),
            random_id=bot.extension.random_id()
        )

        await send_default_keyboard()

        user = await bot.api.users.get(user_ids=[event.user_id])
        Users.add(event.user_id, f'{user[0].first_name} {user[0].last_name}')


@bot.on.message(text=['Меню'])
async def send_default_keyboard(answer: Message):
    await bot.api.messages.send(
        peer_id=answer.peer_id,
        message="Призываем меню",
        keyboard=utils.create_keyboard('Добавить группу', 'Указать адрес', 'Где трамваи?'),
        random_id=bot.extension.random_id()
    )


@bot.on.message(text=['Добавить себя'])
async def add_user(answer: Message):
    if not Users.add(answer.from_user):
        await answer("Возникла ошибка. Попробуй позже")
        return

    await answer("Готово")


@bot.on.message(text=['Указать адрес'])
async def suggest_dorms(answer: Message):
    await answer("Укажите свой адрес")
    await bot.branch.add(answer.peer_id, "address_branch")


@bot.branch.simple_branch("address_branch")
async def update_address(answer: Message):
    if Users.update_address(answer.from_id, answer.text):
        await answer("Готово! Данные занесены в базу")
        await send_default_keyboard(answer)

    await bot.branch.exit(answer.peer_id)


@bot.on.message(text=['Где трамваи?'])
async def show_trolleys(answer: Message):
    keyboard = utils.create_keyboard('Обновить данные', 'Покажи главное меню')
    await answer(messages.trolleys, keyboard=keyboard.generate())


if __name__ == '__main__':
    bot.run_polling()
