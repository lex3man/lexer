
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from mods import api_requests

async def create_keyboard(kb_name, user_id):
    new_kb = ReplyKeyboardMarkup(resize_keyboard = True)
    maximum_lines = 20
    buttons_content = await api_requests.get_content_proxy('RUS', ['kb_buttons', '', user_id])
    buttons = buttons_content[kb_name]
    for i in range(maximum_lines + 1):
        cp = 0
        for key in buttons.keys():
            if buttons[key][1] == i:
                cp += 1
                if cp == 1: new_kb.add(KeyboardButton(buttons[key][0]))
                else: new_kb.insert(KeyboardButton(buttons[key][0]))
    return new_kb

async def get_social_kb(content):
    new_kb = InlineKeyboardMarkup()
    links_cont = content['social_cont']
    for g in links_cont.keys():
        for k in links_cont[g]:
            new_kb.add(InlineKeyboardButton(k, url = links_cont[g][k]))
    return new_kb