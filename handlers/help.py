from aiogram import types, Dispatcher


async def help_command_help(message: types.Message):
    if message.chat.type == types.chat.ChatType.PRIVATE:
        commands_list = [
            '/start - для начала работы, регистрации ментора',
            '/change - для смены месяца обучения ментора',
            '/rating - узнать рейтинг ментора',
            '/rule - правила группы',]

        admin_command_list = [
            '/chart - для розыгрыша заявки студента',
            '/rating - узнать рейтинг менторов',
            '/mentors - узнать сколько менторов на какой месяц',
            '/kick - для удаления участника группы',]

        data = ['<b>Список команд чата:</b>\n для пользователей:']
        for command in commands_list:
            data.append(command)
        data.append('\nдля админов группы:')
        for command in admin_command_list:
            data.append(command)

        data = '\n'.join(data)

        await message.reply(
            text=data,
            parse_mode=types.ParseMode.HTML)

    else:
        await message.reply(
            text='[@GEEKS_BOT](https://t.me/geek_backend_mentor_bot) и используйте команду /help',
            parse_mode=types.ParseMode.MARKDOWN, )


def register_help_handlers(dp: Dispatcher):
    dp.register_message_handler(help_command_help, commands=['help'])
