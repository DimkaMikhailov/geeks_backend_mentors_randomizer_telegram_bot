import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot, group_id
from database.SQLOperator import SQLOperator
import keyboards.kb as kb


class PersonalStudentStates(StatesGroup):
    message = State()
    send_message = State()

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
            reply_markup=await kb.two_button_inline_markup(
                text=['Да', 'Пусть решит случай'],
                callback=['admin_chart_btn_yes', 'admin_chart_btn_no']))


async def admin_action_chart_mentor_list(call: types.CallbackQuery):
    mentors = SQLOperator().select_all_mentors()
    if mentors:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Выбирите ментора',
            reply_markup=await kb.mentors_list_inline_markup(mentors))
    else:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Что-то пошло нет так:(\n'
                 ' Или у нас не осталось менторов!')

    await PersonalStudentStates.message.set()


async def admin_action_check_mentor(call: types.CallbackQuery, state: FSMContext):
    mentor_id = call.data.split('_')[-1]
    winner = SQLOperator().select_one_mentor(user_id=int(mentor_id))
    if winner:
        SQLOperator().update_reqeust()
        SQLOperator().update_wins(user_id=winner['telegram_id'])

        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Перешлите сообщение или контакт студента.!')

        async with state.proxy() as data:
            data['winner'] = winner
            await PersonalStudentStates.next()

            await bot.send_message(
                chat_id=winner['telegram_id'],
                text='Старший ментор персонально передает вам студента:')
    else:
        bot.send_message(
            chat_id=call.message.chat.id,
            text='Чот-то пошло не так. Попробуйте позднее.')


async def admin_action_send_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        winner = data['winner']
        if message.forward_from:
            print(message.forward_from)
            answer = f'Студент: @[{message.forward_from.username}](tg://user?id={message.forward_from.id})\n' \
                     f'{message.text}'
        else:
            answer = message.text
        await state.finish()

        await bot.send_message(
            text=answer,
            chat_id=winner['telegram_id'],
            parse_mode=types.ParseMode.MARKDOWN)


def register_admin_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_action_chart, commands=['chart'])
    dp.register_callback_query_handler(admin_action_chart_mentor_list, lambda call: call.data == 'admin_chart_btn_yes')
    dp.register_callback_query_handler(admin_action_check_mentor, lambda call: 'actions_btn_' in call.data,
                                       state=PersonalStudentStates.message)
    dp.register_message_handler(admin_action_send_message, state=PersonalStudentStates.send_message)