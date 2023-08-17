from aiogram import types, Dispatcher
from config import bot


async def rule_command_rule(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Эта группа для работы менторов backend. \n'
             f'В группе <b>запрещены</b>:\n'
             f'Флуд, спам, реклама, общение на нерабочие темы. Пропаганда и уничижение любого вероисповедания, '
             f'личного мнения, интересов, политических взглядов и т.п.\n'
             f'Будте корректны и взаимовежливы!',
        parse_mode=types.ParseMode.HTML)


def register_rule_handlers(dp: Dispatcher):
    dp.register_message_handler(rule_command_rule, commands=['rule'])
