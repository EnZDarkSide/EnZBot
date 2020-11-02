import json
from typing import Dict

from vkbottle import Message

from src import messages
from src.bot import bot
from src.bot.branch_manager import move_to_branch
from src.database.Portal import DBPortal
from src.portal.parser import PortalManager, format_tasks, try_login
from src.utils import general_keyboard, create_keyboard
from vkbottle.framework import CtxStorage

portal_users = dict()


@bot.on.message(text=['Портал', 'П'])
async def portal(answer: Message):
    user = DBPortal.get(answer.from_id)

    if user is None:
        await update_portal_datа(answer)
    else:
        await get_portal_subjects(answer, user)


async def update_portal_datа(answer: Message):
    await answer(f'Похоже, вам нужно указать данные для входа в портал.'
                 f'Для этого введите через пробел логин и пароль от портала')
    await move_to_branch(answer.peer_id, 'portal_data_update')


async def get_portal_subjects(answer: Message, user):
    try:
        pm = PortalManager(user[0], user[1])
    except ValueError:
        await update_portal_datа(answer)

    subjects = pm.get_sites()

    await move_to_portal_subject(answer, subjects)


async def move_to_portal_subject(answer, subjects):
    await answer('Какой из предметов вас интересует?')
    if len(subjects) > 0:
        await answer('\n'.join([f'{index+1}. {subject["text"]}' for index, subject in enumerate(subjects)]))
    await move_to_branch(answer.peer_id, 'portal_subject')


@bot.branch.simple_branch('portal_subject')
async def get_portal_tasks(answer: Message):
    pp = portal_users[answer.from_id]

    if answer.text.lower() in ['назад']:
        await answer('Возвращаемся', keyboard=general_keyboard())
        await move_to_portal_subject(answer, pp.subjects)
        return

    if not answer.text.isdigit():
        await answer('Введите число')
        return

    if 1 > int(answer.text) > len(pp.subjects):
        await answer(f'Введите число от 1 до {len(pp.subjects)}')
        return

    href = pp.subjects[int(answer.text)-1]['href']
    tasks = format_tasks(pp.get_tasks(href))

    if len(tasks) < 1:
        await answer('У вас нет заданий', keyboard=create_keyboard([{'text': 'Назад'}]))
        await bot.branch.exit(answer.peer_id)
        return

    for task in tasks[:-1]:
        await answer(task)

    await answer(tasks[-1], keyboard=create_keyboard([{'text': 'Назад'}]))
    await move_to_portal_subject(answer, [])


@bot.branch.simple_branch('portal_data_update')
async def portal_data_update(answer: Message):
    if answer.text.lower() in ['назад']:
        await answer('Возвращаемся', keyboard=general_keyboard())
        await bot.branch.exit(answer.peer_id)
        return

    temp = answer.text.split(' ')

    try:
        lgn = temp[0]
        pwd = temp[1]
    except IndexError or ValueError:
        await answer('Похоже, что-то пошло не так. Попробуйте снова', keyboard=create_keyboard([{'text': 'Назад'}]))
        return

    if try_login(lgn, pwd) is False:
        await answer('Похоже, что-то пошло не так. Попробуйте снова', keyboard=create_keyboard([{'text': 'Назад'}]))
        return

    if not DBPortal.add_or_update(answer.from_id, lgn, pwd):
        await answer('Похоже, что-то пошло не так. Попробуйте снова', keyboard=create_keyboard([{'text': 'Назад'}]))
        return

    await answer(messages.done, keyboard=general_keyboard())
    await bot.branch.exit(answer.peer_id)
