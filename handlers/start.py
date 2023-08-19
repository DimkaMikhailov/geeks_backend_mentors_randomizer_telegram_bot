from aiogram import types, Dispatcher
from config import bot, group_id
from database.SQLOperator import SQLOperator
import keyboards.kb as kb


async def is_admin(user_id: types.Message):
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] in ['creator', 'admin'] else False


async def start_command_start(message: types.Message):
    if message.chat.type == types.chat.ChatType.PRIVATE:
        mentor = SQLOperator().select_one_mentor(user_id=message.from_user.id)
        admin = await is_admin(user_id=message.from_user.id)
        if not mentor and not admin:
            await message.reply(
                text=f'День добрый {message.from_user.username if message.from_user.username else "ментор backend"}! '
                     f'Эта группа для работы менторов backend. \n'
                     f'В группе <b>запрещены</b>:\n'
                     f'Флуд, спам, реклама, общение на нерабочие темы. Пропаганда и уничижение любого вероисповедания, '
                     f'личного мнения, интересов, политических взглядов и т.п.\n'
                     f'Будте корректны и взаимовежливы!',
                parse_mode=types.ParseMode.HTML)
            print('add member')
            SQLOperator().insert_into('mentors', (
                False,
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
                False,
                1))

            await bot.send_message(
                chat_id=message.chat.id,
                text='Какой у вас курс?',
                reply_markup=await kb.five_button_inline_markup(
                    text=['2 месяц', '3 месяц', '4 месяц', '5 месяц', 'этот месяц не преподаю'],
                    callback=['start_btn_2', 'start_btn_3', 'start_btn_4', 'start_btn_5', 'start_btn_no']))

        elif mentor and not admin:
            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Привет, {message.from_user.username if message.from_user.username else "ментор"}. '
                     f'Ваш месяц обучения: {mentor["month"]}. '
                     f'Больше информации /help')

        elif not mentor and admin:
            SQLOperator().insert_into('mentors', (
                True,
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
                False,
                256))

            await bot.send_message(
                chat_id=message.chat.id,
                text='Приветствую вас сенсей! Планируете преподавать?',
                reply_markup=await kb.two_button_inline_markup(
                    text=['Да, конечно', 'Этот месяц не преподаю'],
                    callback=['start_btn_yes', 'start_btn_no']))

        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Приветствую вас сенсей! Больше информации /help')

    else:
        await message.reply(
            text='Добро пожаловать в группу GEEKS Backend Mentors! '
                 'Перейдите по ссылке [@GEEKS_BOT](https://t.me/geek_backend_mentor_bot) и используйте команду /start',
            parse_mode=types.ParseMode.MARKDOWN,)


async def start_callback_2_month(call: types.CallbackQuery):
    SQLOperator().update_month(user_id=call.from_user.id, month=2)
    SQLOperator().update_in_chart(user_id=call.from_user.id, in_chart=True)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Отлично, вы ментор для студентов 1 месяца обучения!')


async def start_callback_3_month(call: types.CallbackQuery):
    SQLOperator().update_month(user_id=call.from_user.id, month=3)
    SQLOperator().update_in_chart(user_id=call.from_user.id, in_chart=True)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Отлично, вы ментор для студентов 1-2 месяца обучения!')


async def start_callback_4_month(call: types.CallbackQuery):
    SQLOperator().update_month(user_id=call.from_user.id, month=4)
    SQLOperator().update_in_chart(user_id=call.from_user.id, in_chart=True)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Отлично, вы ментор для студентов 1-3 месяца обучения!')


async def start_callback_5_month(call: types.CallbackQuery):
    SQLOperator().update_month(user_id=call.from_user.id, month=5)
    SQLOperator().update_in_chart(user_id=call.from_user.id, in_chart=True)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Отлично, вы ментор для студентов 1-4 месяца обучения!')


async def start_callback_teach_no(call: types.CallbackQuery):
    SQLOperator().update_in_chart(user_id=call.from_user.id, in_chart=False)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Это будет сложно, но попробуем этот месяц обойтись без вас!')


async def start_callback_teach_yes(call: types.CallbackQuery):
    SQLOperator().update_in_chart(user_id=call.from_user.id, in_chart=True)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='Отлично, вы ментор-сенсей для студентов 1-5 месяца обучения!')


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command_start, commands=['start'])
    dp.register_callback_query_handler(start_callback_2_month, lambda call: call.data == 'start_btn_2')
    dp.register_callback_query_handler(start_callback_3_month, lambda call: call.data == 'start_btn_3')
    dp.register_callback_query_handler(start_callback_4_month, lambda call: call.data == 'start_btn_4')
    dp.register_callback_query_handler(start_callback_5_month, lambda call: call.data == 'start_btn_5')
    dp.register_callback_query_handler(start_callback_teach_no, lambda call: call.data == 'start_btn_no')
    dp.register_callback_query_handler(start_callback_teach_yes, lambda call: call.data == 'start_btn_yes')
