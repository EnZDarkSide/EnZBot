import os

from vkbottle import Bot

from src.groups.groups import bp as groups_bp
from src.portal.portal_endpoint import bp as portal_bp
from src.schedule.schedule_endpoint import bp as schedule_bp
from src.transport.endpoint import bp as trams_bp

API_TOKEN = os.environ['API_TOKEN']

bot = Bot(API_TOKEN)

bot.set_blueprints(portal_bp, schedule_bp, groups_bp, trams_bp)
