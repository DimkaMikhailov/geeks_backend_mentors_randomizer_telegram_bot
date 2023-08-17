from aiogram import types, Dispatcher
from config import bot, group_id
from database.SQLOperator import SQLOperator


async def is_admin(user_id: types.Message):
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] in ['creator', 'admin'] else False


async def in_chat(user_id: types.Message):
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] not in ['kicked', 'left'] else False


async def rating_command_rating(message: types.Message):
    if message.chat.type == types.chat.ChatType.PRIVATE:
        admin = await is_admin(user_id=message.from_user.id)
        mentor = SQLOperator().select_rating_mentor_for(user_id=message.from_user.id)
        print(mentor)
        if admin:
            mentor_list = SQLOperator().select_rating_all_mentors()
            data = ['*Список менторов:*']
            for mentor in mentor_list:
                if not mentor["username"]:
                    data.append(f'{(str(mentor["month"]) + " месяц") if mentor["month"] < 6 else "admin"} '
                                f'[{mentor["first_name"]}](tg://user?id={mentor["telegram_id"]}) - '
                                f'всего: {mentor["request"]} получил: {mentor["wins"]}, отказался: {mentor["failure"]}')
                else:
                    data.append(f'{(str(mentor["month"]) + " месяц") if mentor["month"] < 6 else "admin"} '
                                f'[{mentor["username"]}](tg://user?id={mentor["telegram_id"]}) - '
                                f'всего: {mentor["request"]} получил {mentor["wins"]}, отказался: {mentor["failure"]}')

            data = '\n'.join(data)
            await message.reply(
                text=data,
                parse_mode=types.ParseMode.MARKDOWN)

        else:
            member_in_chat = await in_chat(user_id=message.chat.id)
            if member_in_chat:
                mentor = SQLOperator().select_rating_mentor_for(user_id=message.from_user.id)
                await message.reply(
                    text=f'Ваши результаты:\n'
                         f'Разыграно заявок за месяц: {mentor["requests"]}'
                         f'Поручено студентов: {mentor["win"]}\n'
                         f'Пропущено заявок: {mentor["failure"]}')
                if mentor['win'] > 5:
                    await bot.send_message(
                        text='Отличный результат, так держать!',
                        chat_id=message.chat.id)
    else:
        await message.reply(
            text='Перейдите по ссылке [@GEEKS_BOT](https://t.me/geek_backend_mentor_bot) и используйте команду /rating',
            parse_mode=types.ParseMode.MARKDOWN, )


def register_rating_handlers(dp: Dispatcher):
    dp.register_message_handler(rating_command_rating, commands=['rating'])
