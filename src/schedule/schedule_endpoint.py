from vkbottle.bot import Message, Blueprint
from vkbottle.branch import Branch, ClsBranch, rule_disposal, ExitBranch
from vkbottle.framework.framework.rule import VBMLRule

from src import utils
from src.database.enitities.Groups import DBGroups
from src.database.save_branch import MySqlBranch
from src.schedule import ScheduleManager
from src.utils import general_keyboard

schedule = ScheduleManager().schedules['УрГЭУ']

bp = Blueprint()
bp.branch = MySqlBranch()


@bp.on.message(text=['Расписание', 'Р'])
async def get_schedule(answer: Message):
    await answer('На какой день показать расписание?', keyboard=utils.schedule_keyboard())
    return Branch('schedule_main')


class PortalBranch(ClsBranch):
    async def branch(self, answer: Message, *args):
        request = DBGroups.get(answer.from_id)

        group = request[0]

        buttons_dict = utils.get_schedule_buttons(add_today=True)

        if answer.text in buttons_dict.keys():
            button = buttons_dict[answer.text]

            result = schedule.get_schedule(group, button['start_date'], button['end_date'])
            for r in result:
                await answer(r, keyboard=utils.schedule_keyboard())
        elif answer.text == 'debug':
            str = '\n'.join([f'{btn}: {btn["start_date"]}' for btn in buttons_dict])
            await answer(f'{str}', keyboard=utils.schedule_keyboard())
        else:
            await answer("Шо? Нипонял (пасхалка найдена)", keyboard=utils.schedule_keyboard())

    @rule_disposal(VBMLRule(["выйти", "назад"], lower=True))
    async def exit_branch(self, answer: Message):
        await answer('Возвращаемся', keyboard=general_keyboard())
        return ExitBranch()


bp.branch.add_branch(PortalBranch, "schedule_main")
