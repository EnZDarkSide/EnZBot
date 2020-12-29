# -*- coding: utf-8 -*-
from vkbottle import Message
from vkbottle.branch import Branch

from src.bot import bot
from src.database.enitities import DBGroups
from src.other import messages, keyboards


# приветствие
# добавление нескольких групп
# узнавание рейтинга
# узнавание домашки
# узнавание новой домашки (возможно)
# трамваи
# метро
# настройки


@bot.on.message()
@bot.on.message(text=['Меню', 'Главное меню', '?'])
async def send_menu(answer: Message):
    if not DBGroups.get(answer.from_id):
        await answer('Чтобы продолжить, вам нужно вписать группу для расписания')
        return Branch('groups_update')

    await answer(message=messages.resp_show_menu, keyboard=keyboards.main_menu())


if __name__ == '__main__':
    bot.run_polling()
