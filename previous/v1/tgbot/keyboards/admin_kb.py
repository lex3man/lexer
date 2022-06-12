from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from mods import api_requests

async def make_inline_keyboard(kb_name, usr_id):
    inline_keyboard = InlineKeyboardMarkup()
    return inline_keyboard

async def make_std_keyboard(kb_name, usr_id):
    std_keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
    std_keyboard.add(KeyboardButton('ok'))
    return std_keyboard

async def groups_list(usr_id):
    inline_keyboard = InlineKeyboardMarkup()
    resp = await api_requests.get_groups_info(usr_id)
    if resp['status'] == 'OK':
        grps_info = resp['groups']
        for grp in grps_info.keys():
            grp_inf = grps_info[grp]
            inline_keyboard.add(InlineKeyboardButton(grp_inf['name'] + ': ' + str(grp_inf['members']) + ' человек', callback_data = grp))
        inline_keyboard.add(InlineKeyboardButton('Все пользователи', callback_data = 'all'))
    else: inline_keyboard.add(InlineKeyboardButton('Нет', callback_data = None))
    return inline_keyboard

async def make_list_kb(btn_text):
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True)
    keyboard.add(KeyboardButton(btn_text))
    keyboard.add(KeyboardButton('Назад'))
    return keyboard