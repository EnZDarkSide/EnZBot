from fuzzywuzzy import process
from vkbottle.bot import Message, Blueprint
from vkbottle.branch import ClsBranch, Branch, rule_disposal, ExitBranch
from vkbottle.rule import VBMLRule

import src.database.enitities
from src.other import messages
from src.other.utils import general_keyboard, range_menu, create_keyboard
from src.schedule import ScheduleManager

schedule = ScheduleManager().schedules["УрГЭУ"]

bp = Blueprint()

kb_exit = create_keyboard([{'text': 'Выйти'}])


@bp.on.message(text=['Начать'])
async def send_greetings(answer: Message):
    await answer(messages.send_greetings())

    if not src.database.enitities.DBGroups.get(answer.from_id):
        await answer('Чтобы продолжить, вам нужно вписать группу для расписания')
        return Branch('groups_update')

    await answer('Вы уже вписали свою группу', keyboard=general_keyboard())


@bp.on.message(text=['Сменить группу'])
async def change_group(answer: Message):
    await answer('Чтобы продолжить, вам нужно вписать группу для расписания', keyboard=kb_exit)
    return Branch('groups_update')


@bp.branch.cls_branch("groups_update")
class GroupsUpdate(ClsBranch):
    async def branch(self, answer: Message, *args):
        await update_group(answer)

    @rule_disposal(VBMLRule(["выйти", "назад"], lower=True))
    async def exit_branch(self, answer: Message):
        await answer("Возвращаемся", keyboard=general_keyboard())
        return ExitBranch()


async def update_group(answer: Message):
    group = answer.text
    groups_list = schedule.get_list_of_groups(group)
    similar_groups = process.extract(group, groups_list, limit=5)

    try:
        group_index = [a.lower() for a in groups_list].index(group.lower())
    except ValueError:
        group_index = -1

    if len(groups_list) >= 1 and group_index != -1:
        src.database.enitities.DBGroups.add_or_update(answer.from_id, groups_list[group_index])
    else:
        await answer("Похоже, группы с таким именем не существует.")
        if len(similar_groups) > 0:
            await answer("Возможно, вы имели в виду что-то из этого: \n",
                         keyboard=range_menu([x[0] for x in similar_groups]))
        return

    await answer(messages.done, keyboard=general_keyboard())
    await bp.branch.exit(answer.peer_id)
