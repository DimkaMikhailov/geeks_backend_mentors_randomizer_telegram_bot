from aiogram.utils import executor
from config import dp
from handlers import start, admin_actions, change, help, rating, rule, chart, mentors
from database.SQLOperator import SQLOperator
import database.sql_queries as sql

 # chart - логика на 10 минут
 # start - готов
 # admin_action - готов
 # Написать смену месяца через месяц


async def on_startup(x):
    table_headers = {
        'mentors': sql.mentors_headers,
        'mentors_rating': sql.mentors_rating_headers,
    }

    for name, header in table_headers.items():
        SQLOperator().create_table(name, header)


start.register_start_handlers(dp)
admin_actions.register_admin_actions_handlers(dp)
change.register_change_handlers(dp)
help.register_help_handlers(dp)
rating.register_rating_handlers(dp)
rule.register_rule_handlers(dp)
chart.register_chart_handlers(dp)
mentors.register_mentors_handlers(dp)
# filter for message always at the END

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
