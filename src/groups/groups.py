from fuzzywuzzy import process
from vkbottle import Message

from src import messages
from src.bot import bot
from src.database.Groups import DBGroups
from src.schedule_manager.schedule_manager import ScheduleManager
from src.utils import general_keyboard, range_menu

schedule = ScheduleManager().schedules["УрГЭУ"]


async def update_group(answer: Message):
    group = answer.text
    groups_list = schedule.get_list_of_groups(group)
    similar_groups = process.extract(group, groups_list, limit=5)

    if len(groups_list) == 1:
        DBGroups.add_or_update(answer.from_id, answer.text)
    else:
        await answer("Похоже, группы с таким именем не существует. Возможно, вы имели в виду что-то из этого: \n",
                     keyboard=range_menu([x[0] for x in similar_groups]))
        return

    await answer(messages.done, keyboard=general_keyboard())
    await bot.branch.exit(answer.peer_id)
