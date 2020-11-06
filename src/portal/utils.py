from expiringdict import ExpiringDict
from vkbottle import Message
from vkbottle.branch import Branch

from src.database.enitities.Portal import DBPortal
from src.portal.parser import PortalManager
from src.utils import create_keyboard

portal_users = ExpiringDict(max_len=10000, max_age_seconds=300)

kb_exit = create_keyboard([{'text': 'Выйти'}])
