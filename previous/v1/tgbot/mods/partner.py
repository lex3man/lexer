from aiogram import types, Dispatcher
from mods import api_requests
from mods.other import Scheme_position
from aiogram.dispatcher.filters import Text

# Личный кабинет партнёра

async def get_ref_link(message : types.Message):
    await api_requests.history_record(message.from_user.id, message.text)
    part_info = await api_requests.get_part_info(message.from_user.id)
    rsi_id = int(part_info['rsi_id'])
    info = await api_requests.request_rsi({'pref':'/ref', 'id':rsi_id})
    await message.answer(str(info['data']))

async def view_profile(message : types.Message):
    await api_requests.history_record(message.from_user.id, message.text)
    part_info = await api_requests.get_part_info(message.from_user.id)
    rsi_id = int(part_info['rsi_id'])
    user_info = await api_requests.request_rsi({'pref':'/user/view', 'id':rsi_id})
    user_info = user_info['data']
    part_full_name = user_info['first_name'] + ' ' + user_info['patronymic'] + ' ' + user_info['last_name']
    part_id = str(user_info['user_id'])
    part_email = user_info['email']
    part_phone = user_info['phone']
    part_birthdate = user_info['birthdate']
    content = 'Full name: ' + part_full_name + '\n' + 'ID: ' + part_id + '\n' + 'email: ' + part_email + '\n' + 'Phone: ' + part_phone + '\n' + 'Birthday: ' + part_birthdate
    await message.answer(content)

async def client_invite(message : types.Message):
    await api_requests.history_record(message.from_user.id, message.text)
    part_info = await api_requests.get_part_info(message.from_user.id)
    get_code = part_info['ref_code']
    content = 'https://t.me/rsi_business_bot?start=cli_' + get_code
    await message.answer(content)

async def register_handlers_admin(dp : Dispatcher):
    initializators = await api_requests.get_content_proxy('RUS', 'kb_buttons')

    dp.register_message_handler(get_ref_link, Text(equals = initializators['lk_kb']['RSI_ref_link'][0]), state = Scheme_position.partner_cab)
    dp.register_message_handler(view_profile, Text(equals = initializators['lk_kb']['user_info'][0]), state = Scheme_position.partner_cab)
    dp.register_message_handler(client_invite, Text(equals = initializators['lk_kb']['client_invite'][0]), state = Scheme_position.partner_cab)