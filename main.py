from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram.utils import executor
from config import dp, bot
from handlers import start, admin_actions, change, help, rating, rule, chart, mentors, kick, apscheduler
from database.async_database import Database


async def on_startup(x):
    await Database().init_models()
    scheduler = AsyncIOScheduler(timezone='Asia/Bishkek')
    scheduler.add_job(apscheduler.send_message_every_month,
                      trigger='cron',
                      month='*',
                      day='1',
                      hour='12',
                      minute='0',
                      kwargs={'bot': bot})
    scheduler.start()

start.register_start_handlers(dp)
admin_actions.register_admin_actions_handlers(dp)
change.register_change_handlers(dp)
help.register_help_handlers(dp)
rating.register_rating_handlers(dp)
rule.register_rule_handlers(dp)
chart.register_chart_handlers(dp)
mentors.register_mentors_handlers(dp)
kick.register_kick_handlers(dp)
# filter for message always at the END

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
