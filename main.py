# -*- coding: utf-8 -*-
from vkbottle import Message

from src import messages, utils
from src.bot import bot
from src.bot.branch_manager import move_to_branch
from src.database.Groups import DBGroups
from src.utils import trams_keyboard, general_keyboard
from src.schedule_manager import schedule_menu
from src.transport import Transport


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


@bot.on.message(text=['Меню', 'Главное меню', '?'])
async def send_menu(answer: Message):
    await answer(message=messages.resp_show_menu, keyboard=utils.general_keyboard())


@bot.on.message(text=['Указать адрес'])
async def updating_address_start(answer: Message):
    await answer(messages.getting_address)
    await move_to_branch(answer.peer_id, "updating_address")


@bot.branch.simple_branch("updating_address")
async def update_address(answer: Message):
    if str.lower(answer.text) not in ['назад', 'выйти', 'главное меню', 'меню']:
        if Addresses.add_or_update(answer.from_id, answer.text):
            msg = messages.done
        else:
            msg = messages.error
    else:
        msg = messages.resp_show_menu

    await bot.branch.exit(answer.peer_id)
    await answer(msg, keyboard=general_keyboard())


@bot.on.message(text=['Указать трамвайные остановки'])
async def start_setting_tram_stops(answer: Message):
    await ask_for_home_tram_stop(answer)


async def ask_for_home_tram_stop(answer: Message):
    await answer(messages.asking_for_home_tram_stop)
    await move_to_branch(answer.peer_id, 'asking_for_home_tram_direction')


@bot.branch.simple_branch('asking_for_home_tram_direction')
async def ask_for_home_tram_direction(answer: Message):
    tram_stop = answer.text.lower()

    if Transport.stop_exists(tram_stop):
        tram_directions = Transport.get_directions(tram_stop)
        msg = messages.asking_for_direction
        keyboard = utils.create_keyboard([{"text": tram_direction for tram_direction in tram_directions}])

        await move_to_branch(answer.peer_id, 'setting_home_tram_stop', stop=tram_stop)
    else:
        msg = messages.error
        keyboard = None

    await answer(msg, keyboard=keyboard)


@bot.branch.simple_branch('setting_home_tram_stop')
async def set_home_tram_stop(answer: Message, stop: str):
    stop_id = Transport.get_stop_id(stop, answer.text)
    Addresses.set_home_tram_stop(answer.chat_id, stop_id)
    await ask_for_university_tram_stop(answer)


async def ask_for_university_tram_stop(answer: Message):
    await answer(messages.asking_for_university_tram_stop)
    await move_to_branch(answer.peer_id, 'asking_for_university_tram_direction')


@bot.branch.simple_branch('asking_for_university_tram_direction')
async def ask_for_university_tram_direction(answer: Message):
    tram_stop = answer.text.lower()

    if Transport.stop_exists(tram_stop):
        tram_directions = Transport.get_directions(tram_stop)
        msg = messages.asking_for_direction
        keyboard = utils.create_keyboard([{"text": tram_direction for tram_direction in tram_directions}])

        await move_to_branch(answer.peer_id, 'setting_university_tram_stop', stop=tram_stop)
    else:
        msg = messages.error
        keyboard = None

    await answer(msg, keyboard=keyboard)


@bot.branch.simple_branch('setting_university_tram_stop')
async def set_university_tram_direction(answer: Message, stop: str):
    stop_id = Transport.get_stop_id(stop, answer.text)
    Addresses.set_university_tram_stop(answer.chat_id, stop_id)

    await answer(messages.done)
    await bot.branch.exit(answer.peer_id)


@bot.on.message(text=['Где трамваи?'])
async def show_tram(answer: Message):
    await answer(messages.trams_available, keyboard=trams_keyboard())
    await move_to_branch(answer.peer_id, 'trams_menu')


@bot.branch.simple_branch("trams_menu")
async def show_tram(answer: Message):
    if 'обновить данные' in str.lower(answer.text):
        pass
    elif 'главное меню' in str.lower(answer.text):
        await bot.branch.exit(answer.peer_id)
        await send_menu(answer)
        return

    await answer(messages.trams_available, keyboard=trams_keyboard())


@bot.on.message(text=['Начать'])
async def send_greetings(answer: Message):
    await bot.branch.exit(answer.peer_id)

    user = await bot.api.users.get(user_ids=[answer.from_id])

    await bot.api.messages.send(
        user_id=answer.from_id,
        message=messages.send_greetings(user[0]),
        random_id=bot.extension.random_id()
    )

    if not DBGroups.get(answer.from_id):
        await answer('Чтобы продолжить, вам нужно вписать группу для расписания')
        await move_to_branch(answer.peer_id, 'groups_update')


if __name__ == '__main__':
    bot.run_polling()
