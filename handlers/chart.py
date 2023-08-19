from random import choice
import asyncio
import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import keyboards.kb as kb
from config import bot, group_id
from database.SQLOperator import SQLOperator


class ChartStates(StatesGroup):
    winner = State()
    student = State()
    chart = State()


async def chart_start_fsm(call: types.CallbackQuery):
    await bot.send_message(
        text='Какой месяц у студента?',
        chat_id=call.message.chat.id,
        reply_markup=await kb.five_button_inline_markup(
            text=['1 месяц', '2 месяц', '3 месяц', '4 месяц', '5 месяц'],
            callback=['admin_chart_btn_1', 'admin_chart_btn_2', 'admin_chart_btn_3',
                      'admin_chart_btn_4', 'admin_chart_btn_5']))

    await ChartStates.winner.set()


async def chart_winner_for_1m(call: types.CallbackQuery, state: FSMContext, failure_user=None):
    mentors = SQLOperator().select_mentors_for(1)
    chart_list = []

    for mentor in mentors:
        if mentor['in_chart']:
            member_in_chat = await bot.get_chat_member(chat_id=group_id, user_id=mentor['telegram_id'])
            if member_in_chat['status'] not in ['kicked', 'left']:
                chart_list.append(mentor)

    if failure_user:
        chart_list.remove(failure_user)

    if chart_list:
        winner = choice(tuple(chart_list))
        async with state.proxy() as data:
            data['month'] = 1
            data['winner'] = winner
        await ChartStates.next()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Перешлите сообщение или контакт студента.'
        )

    else:
        await state.finish()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='заявка не разыграна! Попробуйте снова /chart')


async def chart_winner_for_2m(call: types.CallbackQuery, state: FSMContext, failure_user=None):
    mentors = SQLOperator().select_mentors_for(2)
    chart_list = []

    for mentor in mentors:
        if mentor['in_chart']:
            member_in_chat = await bot.get_chat_member(chat_id=group_id, user_id=mentor['telegram_id'])
            if member_in_chat['status'] not in ['kicked', 'left']:
                chart_list.append(mentor)

    if failure_user:
        chart_list.remove(failure_user)
    if chart_list:
        winner = choice(tuple(chart_list))
        async with state.proxy() as data:
            data['month'] = 2
            data['winner'] = winner
        await ChartStates.next()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Перешлите сообщение или контакт студента.')

    else:
        await state.finish()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='заявка не разыграна! Попробуйте снова /chart')


async def chart_winner_for_3m(call: types.CallbackQuery, state: FSMContext, failure_user=None):
    mentors = SQLOperator().select_mentors_for(3)
    chart_list = []

    for mentor in mentors:
        if mentor['in_chart']:
            member_in_chat = await bot.get_chat_member(chat_id=group_id, user_id=mentor['telegram_id'])
            if member_in_chat['status'] not in ['kicked', 'left']:
                chart_list.append(mentor)

    if failure_user:
        chart_list.remove(failure_user)

    if chart_list:
        winner = choice(tuple(chart_list))
        async with state.proxy() as data:
            data['month'] = 3
            data['winner'] = winner
        await ChartStates.next()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Перешлите сообщение или контакт студента.')

    else:
        await state.finish()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='заявка не разыграна! Попробуйте снова /chart')


async def chart_winner_for_4m(call: types.CallbackQuery, state: FSMContext, failure_user=None):
    mentors = SQLOperator().select_mentors_for(4)
    chart_list = []

    for mentor in mentors:
        if mentor['in_chart']:
            member_in_chat = await bot.get_chat_member(chat_id=group_id, user_id=mentor['telegram_id'])
            if member_in_chat['status'] not in ['kicked', 'left']:
                chart_list.append(mentor)

    if failure_user:
        chart_list.remove(failure_user)

    if chart_list:
        winner = choice(tuple(chart_list))
        async with state.proxy() as data:
            data['month'] = 4
            data['winner'] = winner
        await ChartStates.next()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Перешлите сообщение или контакт студента.')

    else:
        await state.finish()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='заявка не разыграна! Попробуйте снова /chart')


async def chart_winner_for_5m(call: types.CallbackQuery, state: FSMContext, failure_user=None):
    mentors = SQLOperator().select_mentors_for(5)
    chart_list = []

    for mentor in mentors:
        if mentor['in_chart']:
            member_in_chat = await bot.get_chat_member(chat_id=group_id, user_id=mentor['telegram_id'])
            if member_in_chat['status'] not in ['kicked', 'left']:
                chart_list.append(mentor)

    if failure_user:
        chart_list.remove(failure_user)

    if chart_list:
        winner = choice(tuple(chart_list))
        async with state.proxy() as data:
            data['month'] = 5
            data['winner'] = winner
        await ChartStates.next()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='Перешлите сообщение или контакт студента.')

    else:
        await state.finish()
        await bot.send_message(
            chat_id=call.message.chat.id,
            text='заявка не разыграна! Попробуйте снова /chart')


async def load_chart_student(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.forward_from:
            student = {
                'username': message.forward_from.username,
                'telegram_id': message.forward_from.id,
                'message': message.text}
        else:
            student = {
                'username': '',
                'telegram_id': '',
                'message': message.text}
        data['student'] = student
        await ChartStates.next()
        winner = data['winner']
        await asyncio.sleep(0.5)
        await bot.send_message(
            text='Вы победили! У вас 10 минут подтвердить готовность, время пошло.\n',
            chat_id=winner['telegram_id'],
            reply_markup=await kb.two_button_inline_markup(
                text=['Забрать', 'Отказаться'],
                callback=['admin_btn_take', 'admin_btn_not_take']))


async def chart_take_student(call: types.CallbackQuery, state: FSMContext):
    SQLOperator().update_reqeust()
    async with state.proxy() as data:
        winner = data['winner']
        SQLOperator().update_wins(user_id=winner['telegram_id'])

        await bot.send_message(
            text=f'Студент {data["month"]} месяц достается достатется '
                 f'*{winner["username"] if winner["username"] else winner["first_name"]}*!',
            chat_id=group_id,
            parse_mode=types.ParseMode.MARKDOWN)

        student = data['student']
        if data['student']:
            if student['username']:
                answer = f'Студент {data["month"]} месяц: [{student["username"]}](tg://user?id={student["telegram_id"]})\n' \
                         f'{student["message"]}'
            else:
                answer = f'Студент {data["month"]} месяц: {student["message"]}'
            await bot.send_message(
                text=answer,
                chat_id=call.message.chat.id,
                parse_mode=types.ParseMode.MARKDOWN)
        else:
            await bot.send_message(
                text='Свяжитесь со старшим ментором для контакта со студентом.',
                chat_id=call.message.chat.id)

    await state.finish()


async def chart_not_take_student(call: types.CallbackQuery, state: FSMContext):
    SQLOperator().update_failure(user_id=call.from_user.id)
    month, failure = 1, None
    async with state.proxy() as data:
        if data:
            month, failure = data['month'], data['winner']
        await state.finish()
    await bot.send_message(
        text='Это будет сложно, но попробуем обойтись без вас!',
        chat_id=call.message.chat.id)
    await ChartStates.winner.set()
    if month == 1:
        await chart_winner_for_1m(call, state, failure_user=failure)
    elif month == 2:
        await chart_winner_for_2m(call, state, failure_user=failure)
    elif month == 3:
        await chart_winner_for_3m(call, state, failure_user=failure)
    elif month == 4:
        await chart_winner_for_4m(call, state, failure_user=failure)
    else:
        await chart_winner_for_5m(call, state, failure_user=failure)


def register_chart_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(chart_start_fsm, lambda call: call.data == 'admin_chart_btn_no')
    dp.register_callback_query_handler(chart_winner_for_1m, state=ChartStates.winner)
    dp.register_callback_query_handler(chart_winner_for_2m, state=ChartStates.winner)
    dp.register_callback_query_handler(chart_winner_for_3m, state=ChartStates.winner)
    dp.register_callback_query_handler(chart_winner_for_4m, state=ChartStates.winner)
    dp.register_callback_query_handler(chart_winner_for_5m, state=ChartStates.winner)
    dp.register_message_handler(load_chart_student, state=ChartStates.student)
    dp.register_callback_query_handler(chart_take_student, lambda call: call.data == 'admin_btn_take',
                                       state=ChartStates.chart)
    dp.register_callback_query_handler(chart_not_take_student, lambda call: call.data == 'admin_btn_not_take',
                                       state=ChartStates.chart)
