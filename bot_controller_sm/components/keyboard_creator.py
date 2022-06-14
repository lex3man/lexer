from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from api_connector import GetContent, AsyncGetContent

async def create_keyboard(bot_name, auth_token, kb_name, user_id):
    keyboards_info = GetContent(bot_name, auth_token, 'keyboard')
    buttons = keyboards_info['keyboard'][kb_name]
    new_kb = ReplyKeyboardMarkup(resize_keyboard = True)
    maximum_lines = 20
    for i in range(maximum_lines + 1):
        cp = 0
        for key in buttons.keys():
            if buttons[key][1] == i:
                cp += 1
                if cp == 1: new_kb.add(KeyboardButton(buttons[key][0]))
                else: new_kb.insert(KeyboardButton(buttons[key][0]))
    return new_kb