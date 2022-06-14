import asyncio
from aiogram import types, Dispatcher
from bot_dispatcher import bot
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from keyboards import other_kb
from mods import api_requests

USER_NAME = None
USER_TAG = None
USER_PREF = None
USER_PHONE = None
USER_ID = None
USER_STATUS = None
CLIENT_SESSON_DATA = {'current_state':''}
GET_STATES = {'next':'2022.02.18.001', 'curent_state':''}

class User(StatesGroup):
    usr_id = State()
    name = State()
    teleg = State()
    usr_tag = State()

class Scheme_position(StatesGroup):
    identity = State()
    new_name = State()
    role_veryfy = State()
    data_collect = State()
    get_input = State()
    partner_cab = State()
    client_way = State()
    admin_mode = State()
    set_schedule_time = State()
    get_sendind_text = State()

# Отмена процесса

async def cancel_handler(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await bot.send_message(message.from_user.id, 'Ok', reply_markup = ReplyKeyboardRemove())

# Регистрация нового пользователя

async def new_usr_reg(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    global USER_TAG
    global USER_PREF
    async with state.proxy() as data:
        data['usr_id'] = message.from_user.id
        data['name'] = message.text
        data['teleg'] = message.from_user.username
        data['usr_tag'] = str(USER_TAG)
    resp_api = await api_requests.reg_usr(data._data)
    answers = await api_requests.get_content_proxy('RUS', 'start_cont')
    if resp_api['status'] == 'OK':
        if resp_api['pref'] == 'None':
            await Scheme_position.role_veryfy.set()
            keyboard = await other_kb.create_keyboard('main_state_kb', message.from_user.id)
            await bot.send_message(message.from_user.id, answers['welcome_message_with_name'] % message.text, reply_markup = keyboard)
        elif resp_api['pref'] == 'cli': # Автоворонка для приглашённых клиентов
            global CLIENT_SESSON_DATA
            CLIENT_SESSON_DATA.update({'usr_id':message.from_user.id})
            USER_PREF = resp_api['pref']
            await Scheme_position.client_way.set()
            CLIENT_SESSON_DATA.update({'current_state':'none'})
            api_resp = await api_requests.get_bot_content('RUS', ['client_way_start_state', 'none' + '__' + CLIENT_SESSON_DATA['current_state'], message.from_user.id])
            kb = await other_kb.create_keyboard('client_way_start_kb', message.from_user.id)
            CLIENT_SESSON_DATA.update({'client_way_start_state':message.text})
            await bot.send_message(message.from_user.id, api_resp['block_cont']['text'] % message.text, reply_markup = kb)
        else:
            await bot.send_message(message.from_user.id, 'No way!', reply_markup = ReplyKeyboardRemove())
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, answers['user_reg_error_message'])

# Редактирование имени

async def change_name(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    global USER_NAME
    answers = await api_requests.get_content_proxy('RUS', 'start_cont')
    if message.text.startswith('Нет'):
        await Scheme_position.next()
        await bot.send_message(message.from_user.id, answers['new_name_please'], reply_markup = ReplyKeyboardRemove())
    else:
        await Scheme_position.role_veryfy.set()
        keyboard = await other_kb.create_keyboard('main_state_kb', message.from_user.id)
        await bot.send_message(message.from_user.id, answers['right_name'] % USER_NAME, reply_markup = keyboard)

async def new_name(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    data = {
        'usr_id':message.from_user.id,
        'name':message.text,
        'head':'update_name'
    }
    resp_api = await api_requests.edit_usr_info(data)
    answers = await api_requests.get_content_proxy('RUS', 'start_cont')
    if resp_api['status'] == 'OK':
        await Scheme_position.role_veryfy.set()
        keyboard = await other_kb.create_keyboard('main_state_kb', message.from_user.id)
        await bot.send_message(message.from_user.id, answers['welcome_message_with_name'] % message.text, reply_markup = keyboard)
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, answers['user_reg_error_message'])

# Соц сети RSI

async def follow_us(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    social_cont = await api_requests.get_bot_content('RUS', ['social_cont', 'get', message.from_user.id])
    if social_cont['status'] == 'OK':
        keyboard = await other_kb.get_social_kb(social_cont)
        await bot.send_message(message.from_user.id, social_cont['text'], reply_markup = keyboard)
        
# Узнать больше о RSI

async def rsi_details(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    detail_cont = await api_requests.get_bot_content('RUS', 'rsi_details')
    if detail_cont['status'] == 'OK':
        keyboard = await other_kb.create_keyboard('rsi_detail_kb', message.from_user.id)
        await bot.send_message(message.from_user.id, detail_cont['text'], reply_markup = keyboard)

# Функции типовых блоков

async def message_sending(message, sets, kb):
    await asyncio.sleep(sets['delay'])
    return bot.send_message(message.from_user.id, sets['text'], reply_markup = kb)

async def standart_block(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    resp_api = await api_requests.get_bot_content('RUS', ['stblck', message.text, message.from_user.id])
    global GET_STATES
    if resp_api['status'] == 'OK':
        sets = resp_api['block_cont']
        kb = await other_kb.create_keyboard(sets['keyboard'], message.from_user.id)
        if sets['input'] == 'no':
            # await message_sending(message, sets, kb)
            await bot.send_message(message.from_user.id, sets['text'], reply_markup = kb)
            if sets['state'] == 'lk_state': await Scheme_position.partner_cab.set()
            else: await Scheme_position.role_veryfy.set()
        else:
            await bot.send_message(message.from_user.id, sets['text'], reply_markup = ReplyKeyboardRemove())
            next_block_id = sets['next']
            GET_STATES.update({'next':next_block_id, 'curent_state':sets['state'], 'usr_id':message.from_user.id, 'tg_username':message.from_user.username, sets['state']:''})
            await Scheme_position.get_input.set()
    else:
        await bot.send_message(message.from_user.id, message.text)

async def save_content(message : types.Message, state : FSMContext):
    await api_requests.history_record(message.from_user.id, message.text)
    global GET_STATES
    # await message.answer(str(GET_STATES))
    curent = GET_STATES['curent_state']
    GET_STATES[curent] = message.text
    # await message.answer(str(GET_STATES))
    resp_api = await api_requests.get_bot_content('RUS', ['block_id', GET_STATES['next'], message.from_user.id])
    if resp_api['status'] == 'OK':
        sets = resp_api['block_cont']
        kb = await other_kb.create_keyboard(sets['keyboard'], message.from_user.id)
        if sets['input'] == 'no':
            await bot.send_message(message.from_user.id, sets['text'], reply_markup = kb)
            await Scheme_position.data_collect.set()
        else:
            await bot.send_message(message.from_user.id, sets['text'], reply_markup = ReplyKeyboardRemove())
            next_block_id = sets['next']
            GET_STATES.update({'next':next_block_id, 'curent_state':sets['state'], sets['state']:''})
            await Scheme_position.get_input.set()
    else:
        await message.answer(GET_STATES[curent])

# Отправка данных

async def send_data(message : types.Message):
    await api_requests.history_record(message.from_user.id, message.text)
    global GET_STATES
    kb = await other_kb.create_keyboard('empty_kb', message.from_user.id)
    # await message.answer(str(GET_STATES))
    resp_api = await api_requests.data_send(GET_STATES)
    await Scheme_position.role_veryfy.set()
    await asyncio.sleep(2)
    await message.answer(resp_api['msg'], reply_markup = kb)

# Проверка на права админа
async def admin_verify(message : types.Message):
    resp = await api_requests.get_usr_info(message.from_user.id)
    if resp['status'] == 'OK':
        if 'admin_group' in resp['groups']: 
            await Scheme_position.admin_mode.set()
            kb = await other_kb.create_keyboard('admin_menu', message.from_user.id)
            await message.answer('You are an Admin!', reply_markup = kb)
        else:
            kb = await other_kb.create_keyboard('empty_kb', message.from_user.id)
            await message.answer('You are not an Admin!', reply_markup = kb)
    else: await message.answer("It's not OK")

async def register_handlers_other(dp : Dispatcher):
    initializators = await api_requests.get_content_proxy('RUS', 'kb_buttons')
    
    # Ввод данных
    dp.register_message_handler(save_content, state = Scheme_position.get_input)
    dp.register_message_handler(send_data, Text(equals = initializators['send_request_kb']['send_request'][0]), state = Scheme_position.data_collect)
    
    # Текстовые команды
    dp.register_message_handler(cancel_handler, Text(equals = 'отмена', ignore_case = True), state = "*")
    dp.register_message_handler(admin_verify, Text(equals = 'sudo', ignore_case = True), state = "*")
    
    dp.register_message_handler(new_usr_reg, state = User.name)
    dp.register_message_handler(change_name, state = Scheme_position.identity)
    dp.register_message_handler(new_name, state = Scheme_position.new_name)

    # Главное меню
    dp.register_message_handler(follow_us, Text(equals = initializators['main_state_kb']['Follow'][0]), state = "*")
    dp.register_message_handler(rsi_details, Text(equals = initializators['main_state_kb']['RSI_details'][0]), state = "*")
    
    # Универсальное условие
    dp.register_message_handler(standart_block, state = "*")