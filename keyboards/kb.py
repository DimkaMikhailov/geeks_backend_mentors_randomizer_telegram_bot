from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def five_button_inline_markup(text: list[str], callback: list[str]):
    if len(text) == 5 and len(callback) == 5:
        button1 = InlineKeyboardButton(text=text[0], callback_data=callback[0])
        button2 = InlineKeyboardButton(text=text[1], callback_data=callback[1])
        button3 = InlineKeyboardButton(text=text[2], callback_data=callback[2])
        button4 = InlineKeyboardButton(text=text[3], callback_data=callback[3])
        button5 = InlineKeyboardButton(text=text[4], callback_data=callback[4])
        markup = InlineKeyboardMarkup()
        markup.add(button1, button2).add(button3, button4)
        markup.add(button5)
        return markup


async def two_button_inline_markup(text: list[str], callback: list[str]):
    if len(text) == 2 and len(callback) == 2:
        button1 = InlineKeyboardButton(text=text[0], callback_data=callback[0])
        button2 = InlineKeyboardButton(text=text[1], callback_data=callback[1])
        markup = InlineKeyboardMarkup()
        markup.add(button1, button2)
        return markup


async def mentors_list_inline_markup(mentors_list, delete_status=False):
    markup = InlineKeyboardMarkup()
    for mentor in mentors_list:
        if mentor.mentor:
            if delete_status:
                check = '❌'
            else:
                check = '✔'
            markup.add(InlineKeyboardButton(
                text=f"{check} {mentor.username if mentor.username else mentor.first_name}",
                callback_data=f'actions_btn_{mentor.telegram_id}'
            ))
    return markup


async def kick_mentors_list_inline_markup(mentors_list, delete_status=False):
    markup = InlineKeyboardMarkup()
    for mentor in mentors_list:
        if mentor.mentor:
            if delete_status:
                check = '❌'
            else:
                check = '✔'
            markup.add(InlineKeyboardButton(
                text=f"{check} {mentor.username if mentor.username else mentor.first_name}",
                callback_data=f'kick_btn_{mentor.telegram_id}'
            ))
    return markup

