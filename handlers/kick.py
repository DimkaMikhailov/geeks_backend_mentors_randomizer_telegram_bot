from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from config import bot, group_id
from database.async_database import Database
import keyboards.kb as kb

class KickMentorState(StatesGroup):
    mentor_id = State()
    kick_mentor = State()


async def is_admin(user_id: int):
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] in ['creator', 'admin'] else False


async def kick_start_command_kick(message: types.Message):
    if message.chat.type == types.chat.ChatType.PRIVATE:
        if await is_admin(user_id=message.from_user.id):
            await bot.send_message(
                chat_id=message.from_user.id,
                text='Вы хотите удалить участника группы?',
                reply_markup=await kb.two_button_inline_markup(
                    text=['Да', 'Нет, я передумал'],
                    callback=['kick_btn_ok', 'kick_btn_no']))

        else:
            await message.reply(
                text='Это команда для админа группы!')
    else:
        await message.reply(
            text='Перейдите по ссылке [@GEEKS_BOT](https://t.me/geek_backend_mentor_bot) и используйте команду /kick',
            parse_mode=types.ParseMode.MARKDOWN, )


async def kick_miss_click(call: types.CallbackQuery, state=None):
    await bot.send_message(
        text='Ок. Увидимся позже',
        chat_id=call.from_user.id)
    if state:
        await state.finish()


async def kick_get_list_members(call: types.CallbackQuery):
    members = await Database().select_all_users()
    mentors = []

    for member in members:
        if member.mentor:
            mentors.append(member)

    await bot.send_message(
        text='Список дествующих менторов:',
        chat_id=call.from_user.id,
        reply_markup=await kb.kick_mentors_list_inline_markup(
            mentors_list=mentors,
            delete_status=True))
    await KickMentorState.mentor_id.set()


async def kick_load_mentors_list(call: types.CallbackQuery, state: FSMContext):
    mentor_id = int(call.data.split('_')[-1])
    async with state.proxy() as data:
        data['mentor_id'] = mentor_id
        await bot.send_message(
            text='Вы уверены, что хотите удалить участника группы?',
            chat_id=call.from_user.id,
            reply_markup=await kb.two_button_inline_markup(
                text=['Да', 'Нет, я передумал'],
                callback=['kick_btb_kick', 'kick_btn_no']))
    await KickMentorState.next()


async def kick_delete_member_from_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.kick_chat_member(chat_id=group_id, user_id=data['mentor_id'])
        await bot.send_message(
            chat_id=message.chat.id,
            text=f'Участник (telegram_id: {data["mentor_id"]}) был удален из группы!')
        await Database().update_user(telegram_id=data['mentor_id'], mentor=False)
    await state.finish()


def register_kick_handlers(dp: Dispatcher):
    dp.register_message_handler(kick_start_command_kick, commands=['kick'])
    dp.register_callback_query_handler(kick_get_list_members, lambda call: call.data == 'kick_btn_ok')
    dp.register_callback_query_handler(kick_miss_click, lambda call: call.data == 'kick_btn_no')
    dp.register_callback_query_handler(kick_load_mentors_list, lambda call: 'kick_btn_' in call.data,
                                       state=KickMentorState.mentor_id)
    dp.register_message_handler(kick_delete_member_from_group, state=KickMentorState.kick_mentor)
