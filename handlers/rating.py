from aiogram import types, Dispatcher
from config import bot, group_id

from database.async_database import Database


async def is_admin(user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] in ['creator', 'admin'] else False


async def in_chat(user_id: int) -> bool:
    member = await bot.get_chat_member(chat_id=group_id, user_id=user_id)
    return True if member['status'] not in ['kicked', 'left'] else False


async def rating_command_rating(message: types.Message):
    if message.chat.type == types.chat.ChatType.PRIVATE:
        admin = await is_admin(user_id=message.from_user.id)
        if admin:
            mentor_list = await Database().select_all_mentors_with_rating()
            data = ['*Список менторов:*']
            for mentor in mentor_list:
                if not mentor['mentor'].username:
                    data.append(
                        f'{(str(mentor["mentor"].month) + " месяц") if mentor["mentor"].month < 6 else "admin"} '
                        f'[{mentor["mentor"].first_name}](tg://user?id={mentor["mentor"].telegram_id}) - '
                        f'всего: {mentor["rating"].request} получил: {mentor["rating"].wins}, отказался: {mentor["rating"].failure}')
                else:
                    data.append(
                        f'{(str(mentor["mentor"].month) + " месяц") if mentor["mentor"].month < 6 else "admin"} '
                        f'[{mentor["mentor"].username}](tg://user?id={mentor["mentor"].telegram_id}) - '
                        f'всего: {mentor["rating"].request} получил: {mentor["rating"].wins}, отказался: {mentor["rating"].failure}')

            data = '\n'.join(data)
            await message.reply(
                text=data,
                parse_mode=types.ParseMode.MARKDOWN)

        else:
            member_in_chat = await in_chat(user_id=message.chat.id)
            if member_in_chat:
                mentor_rating = await Database().select_one_mentor_with_rating(telegram_id=message.from_user.id)

                await message.reply(
                    text=f'*Ваши результаты:*\n'
                         f'Разыграно заявок: {mentor_rating.request}\n'
                         f'Поручено студентов: {mentor_rating.wins}\n'
                         f'Пропущено заявок: {mentor_rating.failure}',
                    parse_mode=types.ParseMode.MARKDOWN)

                if mentor_rating.wins > 5:
                    await bot.send_message(
                        text='Отличный результат, так держать!',
                        chat_id=message.chat.id)
    else:
        await message.reply(
            text='Перейдите по ссылке [@GEEKS_BOT](https://t.me/geek_backend_mentor_bot) и используйте команду /rating',
            parse_mode=types.ParseMode.MARKDOWN, )


def register_rating_handlers(dp: Dispatcher):
    dp.register_message_handler(rating_command_rating, commands=['rating'])
