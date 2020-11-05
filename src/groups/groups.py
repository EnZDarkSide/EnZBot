import src.database.enitities

from fuzzywuzzy import process
from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, Branch, rule_disposal
from vkbottle.rule import VBMLRule

from src import messages
from src.bot import bot
from src.schedule import ScheduleManager
from src.utils import general_keyboard, range_menu

schedule = ScheduleManager().schedules["УрГЭУ"]


bp = Blueprint()


@bp.on.message(text=['Начать'])
async def send_greetings(answer: Message):
    await bot.branch.exit(answer.peer_id)

    await answer(messages.send_greetings(), keyboard=general_keyboard())

    if not src.database.enitities.DBGroups.get(answer.from_id):
        await answer('Чтобы продолжить, вам нужно вписать группу для расписания')
        return Branch('groups_update')

    await answer('Вы уже вписали свою группу', keyboard=general_keyboard())


@bp.branch.cls_branch("groups_update")
class GroupsUpdate(ClsBranch):
    async def branch(self, answer: Message, *args):
        await answer('Чтобы продолжить, вам нужно вписать группу для расписания')

    @rule_disposal(VBMLRule("<group:str>", lower=True))
    async def register(self, answer: Message):
        await update_group(answer)


async def update_group(answer: Message):
    group = answer.text
    groups_list = schedule.get_list_of_groups(group)
    similar_groups = process.extract(group, groups_list, limit=5)

    if len(groups_list) == 1:
        src.database.enitities.DBGroups.add_or_update(answer.from_id, answer.text)
    else:
        await answer("Похоже, группы с таким именем не существует.")
        if len(similar_groups) > 0:
            await answer("Возможно, вы имели в виду что-то из этого: \n",
                         keyboard=range_menu([x[0] for x in similar_groups]))
        return

    await answer(messages.done, keyboard=general_keyboard())
    await bot.branch.exit(answer.peer_id)
