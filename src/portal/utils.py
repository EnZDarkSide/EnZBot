from expiringdict import ExpiringDict
from vkbottle import Message

from src.bot.branch_manager import move_to_branch
from src.database.Portal import DBPortal
from src.portal.parser import PortalManager

portal_users = ExpiringDict(max_len=10000, max_age_seconds=300)


async def get_portal_for_user(answer: Message) -> PortalManager:
    """Получение менеджера портала для пользователя и занесение его во временный кэш"""

    user = DBPortal.get(answer.from_id)
    if user is None:
        await update_portal_data(answer)
    else:
        portal_users[answer.from_id] = PortalManager(user[0], user[1])
    return portal_users[answer.from_id]


async def update_portal_data(answer: Message):
    await answer(f'Похоже, вам нужно указать данные для входа в портал.'
                 f'Для этого введите через пробел логин и пароль от портала')
    await move_to_branch(answer.peer_id, 'portal_data_update')
    return
