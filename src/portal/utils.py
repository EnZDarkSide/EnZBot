from expiringdict import ExpiringDict
from src.other.utils import create_keyboard

portal_users = ExpiringDict(max_len=10000, max_age_seconds=300)

kb_exit = create_keyboard([{'text': 'Выйти'}])
