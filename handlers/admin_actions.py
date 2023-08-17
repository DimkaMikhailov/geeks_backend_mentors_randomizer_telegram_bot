from aiogram import types, Dispatcher
from config import bot, group_id
from database.SQLOperator import SQLOperator
import keyboards.admin_keyboards as kb


async def is_admin(user_id: types.Message):
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] in ['creator', 'admin'] else False


async def in_chat(user_id: types.Message):
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] not in ['kicked', 'left'] else False


async def admin_action_chart(message: types.Message):
    if await is_admin(user_id=message.from_user.id):
        await bot.send_message(
            text='Отдать студента кому-то конкретному?',
            chat_id=message.from_user.id,
            reply_markup=await kb.admin_keyboard_two_button(
                text=['Да', 'Пусть решит случай'],
                callback=['admin_chart_btn_yes', 'admin_chart_btn_no']))


async def admin_action_chart_mentor_list(call: types.CallbackQuery):
    mentors = SQLOperator().select_all_mentors()
    data = []
    for mentor in mentors:
        member_in_chat = await in_chat(user_id=mentor['telegram_id'])
        if member_in_chat:
            if not mentor["username"]:
                data.append(f'[{mentor["first_name"]}](tg://user?id={mentor["telegram_id"]})')
            else:
                data.append(f'[{mentor["username"]}](tg://user?id={mentor["telegram_id"]})')

    data = "\n".join(data)
    if data:
        await bot.send_message(
            text=data,
            chat_id=call.message.chat.id,
            parse_mode=types.ParseMode.MARKDOWN)
    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Что-то пошло нет так:(\n'
                 ' Или у нас не осталось менторов!')


def register_admin_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_action_chart, commands=['chart'])
    dp.register_callback_query_handler(admin_action_chart_mentor_list, lambda call: call.data == 'admin_chart_btn_yes')
