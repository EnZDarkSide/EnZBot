from vkbottle import Message

from src import messages
from src.bot import bot
from src.bot.branch_manager import move_to_branch
from src.database.Portal import DBPortal
from src.portal.parser import format_tasks, try_login
from src.portal.utils import get_portal_for_user
from src.utils import general_keyboard, create_keyboard

kb_exit = create_keyboard([{'text': 'Выйти'}])


@bot.on.message(text=['Портал', 'П'])
async def portal(answer: Message):
    await portal_subjects(answer)


async def portal_subjects(answer, with_subjects=True):
    """Список всех предметов из портала"""
    if answer.text.lower() in ['Выйти']:
        await answer('Главное меню', keyboard=general_keyboard())
        await bot.branch.exit(answer.peer_id)

    pm = await get_portal_for_user(answer)
    if with_subjects:
        subjects = [subj for subj in pm.get_sites()]

        await answer('Какой из предметов вас интересует?')
        if len(subjects) > 0:
            await answer('\n'.join([f'{index+1}. {subject["text"]}' for index, subject in enumerate(subjects)]),
                         keyboard=kb_exit)

    else:
        await answer('Какой из предметов вас интересует?', keyboard=kb_exit)

    await move_to_branch(answer.peer_id, 'portal_tasks')


@bot.branch.simple_branch('portal_tasks')
async def portal_tasks(answer: Message):
    """Получение всех заданий для предмета"""

    pp = await get_portal_for_user(answer)

    if answer.text.lower() in ['выйти']:
        await answer('Возвращаемся', keyboard=general_keyboard())
        await bot.branch.exit(answer.peer_id)
        return

    if not answer.text.isdigit() or 1 > int(answer.text) > len(pp.subjects):
        await answer(f'Введите число от 1 до {len(pp.subjects)}', keyboard=kb_exit)
        return

    href = pp.subjects[int(answer.text)-1]['href']
    tasks = format_tasks(pp.get_tasks(href))

    if len(tasks) < 1:
        await answer('У вас нет заданий', keyboard=kb_exit)
        await bot.branch.exit(answer.peer_id)

    for task in tasks[:-1]:
        await answer(task)

    # Получаем меню вместе с последним сообщением
    await answer(tasks[-1])
    await portal_subjects(answer, with_subjects=False)


@bot.branch.simple_branch('portal_data_update')
async def portal_data_update(answer: Message):
    if answer.text.lower() in ['выйти']:
        await answer('Возвращаемся', keyboard=general_keyboard())
        await bot.branch.exit(answer.peer_id)
        return

    temp = answer.text.split(' ')

    # Попытка войти на портал (без сохранения менеджера)
    if len(temp) != 2 or try_login(temp[0], temp[1]) is False:
        await answer('Похоже, что-то пошло не так. Попробуйте снова', keyboard=kb_exit)
        return

    # Попытка добавить в базу логин и пароль
    if not DBPortal.add_or_update(answer.from_id, temp[0], temp[1]):
        await answer('Похоже, при добавлении записи в базу что-то пошло не так.'
                     ' Попробуйте снова', kb_exit)
        return

    await answer(messages.done, keyboard=general_keyboard())
    await bot.branch.exit(answer.peer_id)
