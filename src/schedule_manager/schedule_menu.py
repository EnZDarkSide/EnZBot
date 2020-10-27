import calendar
import json
from itertools import chain

from vkbottle import Message

from src import utils
from src.bot import bot
from src.bot.branch_manager import move_to_branch
from src.database.Groups import DBGroups
from src.schedule_manager.schedule_manager import ScheduleManager
from src.utils import general_keyboard, b_arr

schedule = ScheduleManager().schedules['УрГЭУ']

schedule_menu_obj = None


@bot.on.message(text=['Расписание', 'Р'])
async def get_schedule(answer: Message):
    await answer('На какой день показать расписание?', keyboard=utils.schedule_keyboard())
    await move_to_branch(answer.peer_id, 'schedule_main')


@bot.on.message(text=['Расписание на <date>', 'Р <date>'])
async def get_schedule(answer: Message, date):
    await move_to_branch(answer.peer_id, 'schedule_main')
    await get_schedule(answer)


@bot.branch.simple_branch('schedule_main')
async def get_schedule(answer: Message):
    if answer.text.lower() in ['назад']:
        await answer('Возвращаемся', keyboard=general_keyboard())
        await bot.branch.exit(answer.peer_id)
        return

    request = await DBGroups.get(answer.from_id)

    if request is None:
        await answer(f'Ошибка, {request}', keyboard=utils.schedule_keyboard())

    group = request[0]

    if answer.text in b_arr:
        pl = json.loads(answer.payload)
        result = schedule.get_schedule(group, pl['start_date'], pl['end_date'])
        for r in result:
            await answer(r, keyboard=utils.schedule_keyboard())
