import pandas as pd

from datetime import datetime

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, ExitBranch, Branch
from vkbottle.branch import rule_disposal
from vkbottle.rule import VBMLRule

from src.other import utils, messages
from src.database.enitities.Portal import DBPortal
from src.portal.parser import try_login, format_tasks, PortalManager
from src.portal.utils import portal_users
from src.other.utils import general_keyboard, create_keyboard, portal_keyboard, schedule_keyboard

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
        return await p_tasks_by_day(answer)

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
            return Branch('portal_tasks')

    @rule_disposal(VBMLRule("выйти", lower=True))
    async def exit_branch(self, answer: Message):
        await answer("Возвращаемся", keyboard=portal_keyboard())
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
    subj_w_tasks = []

    pp = await get_portal_for_user(answer)

    if not pp:
        return

    buttons_dict = utils.get_schedule_buttons(add_today=True)

    if answer.text not in buttons_dict.keys():
        await answer('Воспользуйтесь клавиатурой для выбора даты', keyboard=schedule_keyboard())
        return

    button = buttons_dict[answer.text]

    subjects = await pp.get_subjects()

    start_date_str = button['start_date']
    start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
    dates = [start_date]

    if answer.text.lower() in ['на след. нед.', 'на нед.']:
        timestamps = pd.date_range(start_date, periods=7, tz=tz).tolist()
        dates = [d.date() for d in timestamps]

    try:
        subj_w_tasks = [x for x in [{'subject': subject.name, 'tasks': subject.get_by_date_arr(dates)}
                        for subject in subjects] if x['tasks']]
    except IndexError:
        await answer('Раздел заданий для этого предмета не открыт', keyboard=schedule_keyboard())

    if not subj_w_tasks:
        await answer(f'Заданий нет', keyboard=schedule_keyboard())
        return

    for i, subj in enumerate(subj_w_tasks):
        await answer(f'{"_"*15}\nПредмет: {subj["subject"]}')

        for task in subj['tasks']:
            await answer(task.to_str())

    await answer(f'Это все задания', keyboard=schedule_keyboard())


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

    await answer(messages.done, keyboard=schedule_keyboard())
    await get_portal_for_user(answer)
    return True


async def get_portal_for_user(answer: Message):
    """Получение менеджера портала для пользователя и занесение его во временный кэш"""
    # Если сессия еще жива, взять из кэша

    pm = portal_users.get(answer.from_id)
    if pm:
        return pm

    user = DBPortal.get(answer.from_id)

    if user is None:
        await update_portal_data(answer)
        return None
    else:
        await answer(f'Идет загрузка данных из вашего портала...')
        if DBPortal.get_hint_shown(answer.from_id)[0] == 0:
            await answer(f'Подсказка: Обычно загрузка занимает 3-12 секунд. Чтобы загрузка шла быстрее, нужно'
                         f' убрать из видимых сайтов те предметы, которые больше не идут.'
                         f'\nЭто можно сделать в разделе "Мои настройки" на портале')
            DBPortal.set_hint_shown(answer.from_id)
        pm = await PortalManager().create(user[0], user[1])
        portal_users[answer.from_id] = pm
        return pm


async def update_portal_data(answer: Message):
    await answer(f'Похоже, вам нужно указать данные для входа в портал.'
                 f'Для этого введите через пробел логин и пароль от портала', keyboard=kb_exit)
    await bp.branch.add(answer.peer_id, 'portal_login')