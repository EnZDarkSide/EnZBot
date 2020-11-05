import pandas as pd

from datetime import datetime

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src import messages
from src.database.enitities.Portal import DBPortal
from src.portal.parser import try_login, format_tasks
from src.portal.utils import get_portal_for_user
from src.utils import general_keyboard, create_keyboard, portal_keyboard, schedule_keyboard, b_arr

from src._date import tz

kb_exit = create_keyboard([{'text': 'Выйти'}])

bp = Blueprint()


@bp.on.message(text=['Портал', 'П'])
async def portal(answer: Message):
    await answer('Меню портала', keyboard=portal_keyboard())
    return Branch('portal_menu')


@bp.branch.cls_branch("portal_menu")
class PortalBranch(ClsBranch):
    # @rule_disposal(VBMLRule("предметы", lower=True))
    # async def subjects_tasks_branch(self, answer: Message):
    #     await answer('Какой из предметов вас интересует?', keyboard=schedule_keyboard())
    #     await portal_subjects(answer)
    #     return Branch('portal_tasks')

    @rule_disposal(VBMLRule("расписание заданий", lower=True))
    async def subjects_tasks_branch(self, answer: Message):
        await answer('Выберите день', keyboard=schedule_keyboard())
        return Branch('portal_tasks')

    @rule_disposal(VBMLRule("Сменить данные", lower=True))
    async def register(self, answer: Message):
        await answer('Введите логин и пароль от портала', keyboard=kb_exit)
        return Branch('portal_login')

    @rule_disposal(VBMLRule("выйти", lower=True))
    async def exit_branch(self, answer: Message):
        await answer("Возвращаемся", keyboard=general_keyboard())
        return ExitBranch()

    async def branch(self, answer: Message, *args):
        await portal(answer)


@bp.branch.cls_branch("portal_tasks")
class PortalTasks(ClsBranch):
    async def branch(self, answer: Message, *args):
        await p_tasks_by_day(answer)

    @rule_disposal(VBMLRule(["выйти", "назад"], lower=True))
    async def exit_branch(self, answer: Message):
        await portal(answer)
        return Branch('portal_menu')


@bp.branch.cls_branch("portal_login")
class PortalUserLogin(ClsBranch):
    async def branch(self, answer: Message, *args):
        await answer('Ваших учетных данных нет в базе. Введите логин и пароль от портала,'
                     ' чтобы иметь доступ к заданиям из бота', keyboard=kb_exit)

    @rule_disposal(VBMLRule("<login> <password>", lower=True))
    async def register(self, answer: Message, login, password):
        if await portal_data_update(answer, login, password):
            return Branch('portal_menu')

    @rule_disposal(VBMLRule("выйти", lower=True))
    async def exit_branch(self, answer: Message):
        await answer("Возвращаемся", keyboard=general_keyboard())
        return Branch("portal_menu")


async def portal_subjects(answer):
    pm = await get_portal_for_user(answer)
    if pm is None:
        return

    subjects = await pm.get_subjects()

    if len(subjects) > 0:
        await answer('\n'.join([f'{index + 1}. {subject["text"]}' for index, subject in enumerate(subjects)]),
                     keyboard=kb_exit)


async def p_tasks_by_day(answer: Message):
    """Получение всех заданий для предмета на дату"""
    if answer.text not in b_arr:
        await answer('Воспользуйтесь клавиатурой для выбора даты', keyboard=schedule_keyboard())
        return

    pp = await get_portal_for_user(answer)

    await answer(f'Идет загрузка данных из вашего портала...')

    payload = answer.get_payload_json()
    subjects = await pp.get_subjects()

    try:
        start_date_str = payload['start_date']
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        if answer.text.lower() in ['на след. нед.', 'на нед.']:
            timestamps = pd.date_range(start_date, periods=7, tz=tz).tolist()
            date_list = [d.date() for d in timestamps]
            subj_w_tasks = [{'subject': subject.name, 'tasks': subject.get_by_date_arr(date_list)}
                            for subject in subjects]
        else:
            subj_w_tasks = [{'subject': subject.name, 'tasks': subject.get_by_date_arr([start_date])}
                            for subject in subjects]

        subj_w_tasks = [x for x in subj_w_tasks if x['tasks']]

        if not subj_w_tasks:
            await answer(f'{answer.text.lower()} заданий нет', keyboard=schedule_keyboard())
            return

        for i, subj in enumerate(subj_w_tasks):
            await answer(f'{"_"*15}\nПредмет: {subj["subject"]}')

            for task in subj['tasks']:
                await answer(task.to_str())

        await answer(f'Это все задания {answer.text.lower()}', keyboard=schedule_keyboard())

    except IndexError:
        await answer('Раздел заданий для этого предмета не открыт', keyboard=schedule_keyboard())


async def portal_tasks(answer: Message, subject_number: int):
    """Получение всех заданий для предмета"""
    pp = await get_portal_for_user(answer)

    if subject_number not in range(1, len(pp.subjects) + 1):
        await answer(f'Введите число от 1 до {len(pp.subjects)}', keyboard=kb_exit)
        return

    subject = pp.subjects[subject_number - 1]
    await answer(f'Задания для предмета {subject["text"]}\n')

    try:
        tasks = format_tasks(await pp.get_tasks(subject))

        if len(tasks) == 0:
            await answer('У вас нет заданий для этого предмета', keyboard=kb_exit)

        for task in tasks:
            await answer(task, keyboard=schedule_keyboard())

    except IndexError:
        await answer('Раздел заданий для этого предмета не открыт', keyboard=kb_exit)


async def portal_data_update(answer: Message, login, password):
    # Попытка войти на портал (без сохранения менеджера)
    if not await try_login(login, password):
        await answer('Не удалось войти в систему. Попробуйте снова', keyboard=kb_exit)
        return False

    # Попытка добавить в базу логин и пароль
    if not DBPortal.add_or_update(answer.from_id, login, password):
        await answer('Похоже, при добавлении записи в базу что-то пошло не так.'
                     ' Попробуйте снова', kb_exit)
        return False

    await answer(messages.done, keyboard=general_keyboard())
    return True
