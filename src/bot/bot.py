from vkbottle import Bot
from src.portal.portal_endpoint import bp as portal_bp
from src.schedule.schedule_endpoint import bp as schedule_bp
from src.groups.groups import bp as groups_bp

API_TOKEN = "***REMOVED***"

bot = Bot(API_TOKEN)

bot.set_blueprints(portal_bp, schedule_bp, groups_bp)
