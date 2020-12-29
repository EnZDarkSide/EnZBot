from vkbottle.bot import Message, Blueprint
from vkbottle.branch import Branch, ClsBranch, rule_disposal, ExitBranch
from vkbottle.framework.framework.rule import VBMLRule

import src.other.keyboards
from src.database.enitities.Groups import DBGroups
from src.other import utils, keyboards
from src.schedule import ScheduleManager

schedule = ScheduleManager().schedules['УрГЭУ']

bp = Blueprint()


@bp.on.message(text=['Расписание', 'Р'])
async def get_schedule(answer: Message):
    await answer('На какой день показать расписание?', keyboard=src.other.keyboards.schedule())
    return Branch('schedule_main')


@bp.branch.cls_branch("schedule_main")
class PortalBranch(ClsBranch):
    async def branch(self, answer: Message, *args):
        request = DBGroups.get(answer.from_id)

        group = request[0]

        buttons_dict = utils.get_schedule_buttons(add_today=True)

        if answer.text in buttons_dict.keys():
            button = buttons_dict[answer.text]

            result = schedule.get_schedule(group, button['start_date'], button['end_date'])
            for r in result:
                await answer(r, keyboard=src.other.keyboards.schedule())
        elif answer.text == 'debug':
            str = '\n'.join([f'{btn}: {btn["start_date"]}' for btn in buttons_dict])
            await answer(f'{str}', keyboard=src.other.keyboards.schedule())
        else:
            await answer("Шо? Нипонял (пасхалка найдена)", keyboard=src.other.keyboards.schedule())

    @rule_disposal(VBMLRule(["выйти", "назад"], lower=True))
    async def exit_branch(self, answer: Message):
        await answer('Возвращаемся', keyboard=keyboards.main_menu())
        return ExitBranch()
