from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from mods import api_requests
from mods.other import Scheme_position, CLIENT_SESSON_DATA
from keyboards import other_kb
from aiogram.dispatcher.filters import Text

async def auto_block(message : types.Message):
    global CLIENT_SESSON_DATA
    await api_requests.history_record(message.from_user.id, message.text)
    api_resp = await api_requests.get_bot_content('RUS', ['client_way_start_state', message.text + '__' + CLIENT_SESSON_DATA['current_state'], message.from_user.id])
    CLIENT_SESSON_DATA.update({CLIENT_SESSON_DATA['current_state']:message.text, 'current_state':api_resp['block_cont']['state']})
    try:
        kb = await other_kb.create_keyboard(api_resp['block_cont']['keyboard'], message.from_user.id)
        await message.answer(api_resp['block_cont']['text'], reply_markup = kb)
    except:
        await message.answer(api_resp['block_cont']['text'], reply_markup = ReplyKeyboardRemove())
    await Scheme_position.client_way.set()
    if api_resp['block_cont']['input_data']:
        CLIENT_SESSON_DATA.update({'head':CLIENT_SESSON_DATA['current_state']})
        resp = await api_requests.edit_usr_info(CLIENT_SESSON_DATA)
        if resp['status'] == 'OK': await Scheme_position.role_veryfy.set()

async def go_to_mm(message : types.Message):
    api_resp = await api_requests.get_bot_content('RUS', ['stblck', 'Главное меню', message.from_user.id])
    kb = await other_kb.create_keyboard(api_resp['block_cont']['keyboard'], message.from_user.id)
    await message.answer(api_resp['block_cont']['text'], reply_markup = kb)
    await Scheme_position.role_veryfy.set()

async def register_handlers_client(dp : Dispatcher):
    
    initializators = await api_requests.get_content_proxy('RUS', 'kb_buttons')
    
    dp.register_message_handler(go_to_mm, Text(equals = initializators['Lets_test_state_kb']['Skip'][0]), state = Scheme_position.client_way)
    dp.register_message_handler(auto_block, state = Scheme_position.client_way)