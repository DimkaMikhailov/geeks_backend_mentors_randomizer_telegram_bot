from aiogram import types, Dispatcher
from config import bot
import keyboards.kb as kb


async def change_command_change(message: types.Message):
    if message.chat.type == types.chat.ChatType.PRIVATE:
        await message.reply(
            text='Вы хотите сменить свой месяц обучения?',
            reply_markup=await kb.two_button_inline_markup(
                text=['Да', 'Нет, я ошибся'],
                callback=['change_btn_yes', 'change_btn_no']))

    else:
        await message.reply(
            text='[@GEEKS_BOT](https://t.me/geek_backend_mentor_bot) и используйте команду /change',
            parse_mode=types.ParseMode.MARKDOWN, )


async def change_command_change_yes(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Какой у вас курс?',
        reply_markup=await kb.five_button_inline_markup(
            text=['2 месяц', '3 месяц', '4 месяц', '5 месяц', 'этот месяц не преподаю'],
            callback=['start_btn_2', 'start_btn_3', 'start_btn_4', 'start_btn_5', 'start_btn_no']))


async def change_command_change_no(call: types.CallbackQuery):
    await bot.send_message(
        text='Ни каких проблем. Если что, обращайтесь :)',
        chat_id=call.message.chat.id)


def register_change_handlers(dp: Dispatcher):
    dp.register_message_handler(change_command_change, commands=['change'])
    dp.register_callback_query_handler(change_command_change_yes, lambda call: call.data == 'change_btn_yes')
    dp.register_callback_query_handler(change_command_change_no, lambda call: call.data == 'change_btn_no')
