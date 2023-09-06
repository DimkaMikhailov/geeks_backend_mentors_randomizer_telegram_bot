from aiogram import Bot
from config import group_id


async def send_message_every_month(bot: Bot):
    await bot.send_message(
        text='Менторы, не забудьте сменить ваш месяц обучения, используя команду /change',
        chat_id=group_id)
