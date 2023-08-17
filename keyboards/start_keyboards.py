from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def start_keyboard_five_button(text: list[str], callback: list[str]):
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


async def start_keyboard_two_button(text: list[str], callback: list[str]):
    if len(text) == 2 and len(callback) == 2:
        button1 = InlineKeyboardButton(text=text[0], callback_data=callback[0])
        button2 = InlineKeyboardButton(text=text[1], callback_data=callback[1])
        markup = InlineKeyboardMarkup()
        markup.add(button1, button2)
        return markup
