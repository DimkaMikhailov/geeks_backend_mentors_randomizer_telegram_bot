from aiogram import types, Dispatcher
from config import bot, group_id
from database.SQLOperator import SQLOperator


async def is_admin(user_id: types.Message):
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] in ['creator', 'admin'] else False


async def start_command_mentors(message: types.Message):
    if message.chat.type == types.chat.ChatType.PRIVATE:
        admin = await is_admin(user_id=message.from_user.id)
        if admin:
            mentor_list = SQLOperator().select_rating_all_mentors()
            month1 = ['Для 1 месяца:']
            month2 = ['Для 2 месяца:']
            month3 = ['Для 3 месяца:']
            month4 = ['Для 4 месяца:']
            month5 = ['Для 5 месяца:']
            data = ['*Список менторов:*']
            for mentor in mentor_list:
                if mentor["month"] > 1:
                    if not mentor["username"]:
                        month1.append(f'[{mentor["first_name"]}](tg://user?id={mentor["telegram_id"]})')
                    else:
                        month1.append(f'[{mentor["username"]}](tg://user?id={mentor["telegram_id"]})')
                if mentor["month"] > 2:
                    if not mentor["username"]:
                        month2.append(f'[{mentor["first_name"]}](tg://user?id={mentor["telegram_id"]})')
                    else:
                        month2.append(f'[{mentor["username"]}](tg://user?id={mentor["telegram_id"]})')
                if mentor["month"] > 3:
                    if not mentor["username"]:
                        month3.append(f'[{mentor["first_name"]}](tg://user?id={mentor["telegram_id"]})')
                    else:
                        month3.append(f'[{mentor["username"]}](tg://user?id={mentor["telegram_id"]})')
                if mentor["month"] > 4:
                    if not mentor["username"]:
                        month4.append(f'[{mentor["first_name"]}](tg://user?id={mentor["telegram_id"]})')
                    else:
                        month4.append(f'[{mentor["username"]}](tg://user?id={mentor["telegram_id"]})')
                if mentor["month"] > 5:
                    if not mentor["username"]:
                        month5.append(f'[{mentor["first_name"]}](tg://user?id={mentor["telegram_id"]})')
                    else:
                        month5.append(f'[{mentor["username"]}](tg://user?id={mentor["telegram_id"]})')

            for month in (month1, month2, month3, month4, month5):
                if len(month) > 1: data += month
            data = '\n'.join(data)
            await message.reply(
                text=data,
                parse_mode=types.ParseMode.MARKDOWN)

        else:
            await bot.send_message(
                text='Эта команда только для администраторов группы.',
                chat_id=message.chat.id)
    else:
        await message.reply(
            text='Перейдите по ссылке [@GEEKS_BOT](https://t.me/geek_backend_mentor_bot) и используйте команду /mentors',
            parse_mode=types.ParseMode.MARKDOWN, )


def register_mentors_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command_mentors, commands=['mentors'])
