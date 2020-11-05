from expiringdict import ExpiringDict
from vkbottle import Message
from vkbottle.branch import Branch

from src.database.enitities.Portal import DBPortal
from src.portal.parser import PortalManager
from src.utils import create_keyboard

portal_users = ExpiringDict(max_len=10000, max_age_seconds=300)

kb_exit = create_keyboard([{'text': 'Выйти'}])


async def get_portal_for_user(answer: Message) -> PortalManager:
    """Получение менеджера портала для пользователя и занесение его во временный кэш"""
    # Если сессия еще жива, взять из кэша
    if answer.from_id in portal_users.keys():
        return portal_users[answer.from_id]

    user = DBPortal.get(answer.from_id)
    if user is None:
        await update_portal_data(answer)
    else:
        portal_users[answer.from_id] = await PortalManager().create(user[0], user[1])
    return portal_users[answer.from_id]


async def update_portal_data(answer: Message):
    await answer(f'Похоже, вам нужно указать данные для входа в портал.'
                 f'Для этого введите через пробел логин и пароль от портала', keyboard=kb_exit)
    return Branch('portal_data_update')

