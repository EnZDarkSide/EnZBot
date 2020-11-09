import json

from vkbottle.bot import Message, Blueprint
from vkbottle.branch import Branch, ClsBranch, rule_disposal, ExitBranch
from vkbottle.framework.framework.rule import VBMLRule

from src import utils
from src.database.enitities.Groups import DBGroups
from src.schedule import ScheduleManager
from src.utils import general_keyboard

schedule = ScheduleManager().schedules['УрГЭУ']

bp = Blueprint()


@bp.on.message(text=['Расписание', 'Р'])
async def get_schedule(answer: Message):
    await answer('На какой день показать расписание?', keyboard=utils.schedule_keyboard())
    return Branch('schedule_main')


@bp.branch.cls_branch("schedule_main")
class PortalBranch(ClsBranch):
    async def branch(self, answer: Message, *args):
        request = DBGroups.get(answer.from_id)

        if request is None:
            await answer(f'Ошибка, {request}', keyboard=utils.schedule_keyboard())

        group = request[0]

        if answer.text in utils.get_b_arr():
            pl = json.loads(answer.payload)
            result = schedule.get_schedule(group, pl['start_date'], pl['end_date'])
            for r in result:
                await answer(r, keyboard=utils.schedule_keyboard())
        else:
            await answer("Шо? Нипонял (пасхалка найдена)", keyboard=utils.schedule_keyboard())

    @rule_disposal(VBMLRule(["выйти", "назад"], lower=True))
    async def exit_branch(self, answer: Message):
        await answer('Возвращаемся', keyboard=general_keyboard())
        return ExitBranch()
