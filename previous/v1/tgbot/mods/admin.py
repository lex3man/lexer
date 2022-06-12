from aiogram import types, Dispatcher
from bot_dispatcher import bot
from aiogram.types import ReplyKeyboardRemove
from mods import api_requests, sending
from mods.other import Scheme_position
from keyboards import admin_kb, other_kb
from aiogram.dispatcher.filters import Text
from datetime import date, datetime
import asyncio

SENDING_MODE = None
SENGING_GROUPS = []
SCHEDULE_TIME = None
SENDING_TEXT = None

async def wait_until(time):
    sched_dt = datetime(int(time[2]), int(time[1]), int(time[0]), int(time[3]), int(time[4]), 0, 0)
    send_delay = (sched_dt - datetime.now()).total_seconds()
    await asyncio.sleep(send_delay)
    
async def run_at(time, func, msg):
    await msg.answer('Запустится ' + str(time[0]) + '.' + str(time[1]) + '.' + str(time[2]) + ' в ' + str(time[3]) + ':' + str(time[4]) + ' МСК')
    await wait_until(time)
    return await func

MAKE_LIST_BUTTON_TEXT = 'Сформировать список пользователей'
LIST_CONFORM_BUTTON_TEXT = 'Подтвердить'
CREATE_SENDING_BUTTON_TEXT = 'Создать рассылку'

async def admin_cpanel(message : types.Message):
    await message.answer(
        '''https://lexer.insiderlab.ru/admin
        user: "rsi_admin"
        pass: "rsicapital2000"''')

async def sendings(message : types.Message):
    global SENGING_GROUPS
    SENGING_GROUPS = []
    kb = await other_kb.create_keyboard('sendings_kb', message.from_user.id)
    await message.answer('Прямо сейчас сделать рассылку?', reply_markup = kb)

async def set_schedule(message : types.Message):
    global SENDING_MODE
    await Scheme_position.set_schedule_time.set()
    SENDING_MODE = 'later'
    await message.answer('Впишите время запуска рассылки в формате ДД.ММ.ГГГГ чч:мм\nНапример, "22.11.2022 18:25"', reply_markup = ReplyKeyboardRemove())

async def get_sending_time(message : types.Message):
    global SCHEDULE_TIME
    SCHEDULE_TIME = message.text
    SCHEDULE_TIME_SHOW = SCHEDULE_TIME.split(' ')
    kb = await admin_kb.make_list_kb(LIST_CONFORM_BUTTON_TEXT)
    await message.answer('OK, рассылка запустится ' + str(SCHEDULE_TIME_SHOW[0]) + ' в ' + str(SCHEDULE_TIME_SHOW[1]) + ' МСК', reply_markup = kb)
    SCHEDULE_TIME = SCHEDULE_TIME.replace(' ','.').replace(':','.').split('.')
    # await message.answer('OK' + str(SCHEDULE_TIME))

async def group_choise(message : types.Message):
    global SENDING_MODE
    initializators = await api_requests.get_content_proxy('RUS', 'kb_buttons')
    kb1 = await admin_kb.groups_list(message.from_user.id)
    kb2 = await admin_kb.make_list_kb(MAKE_LIST_BUTTON_TEXT)
    mode = message.text
    if mode == initializators['sendings_kb']['right_now'][0]: SENDING_MODE = 'now'
    # if mode == initializators['sendings_kb']['schedule_message'][0]: SENDING_MODE = 'later'
    await message.answer('Хорошо,', reply_markup = kb2)
    await message.answer('По каким группам сделать рассылку? (можно выбрать несколько)', reply_markup = kb1)
    await Scheme_position.admin_mode.set()

async def get_sending_groups(callback : types.CallbackQuery):
    global SENGING_GROUPS
    if str(callback.data) == 'all':
        SENGING_GROUPS = []
        await bot.answer_callback_query(callback.id, text = 'Рассылка будет по всем пользователям!', show_alert = True)
        SENGING_GROUPS.append(callback.data)
    else:
        SENGING_GROUPS.append(str(callback.data))
        resp = await api_requests.get_groups_info(callback.from_user.id)
        if resp['status'] == 'OK':
            grps_info = resp['groups']
            name = grps_info[str(callback.data)]['name']
        await bot.answer_callback_query(callback.id, text = 'Группа %s добавлена к списку для рассылки' % name.upper(), show_alert = True)

async def make_list_result(message : types.Message):
    global SENGING_GROUPS
    resp = await api_requests.get_groups_info(message.from_user.id)
    grps_info = resp['groups']
    kb = await admin_kb.make_list_kb(LIST_CONFORM_BUTTON_TEXT)
    if 'all' in SENGING_GROUPS: await message.answer('Рассылка будет по всем пользователям', reply_markup = kb)
    else:
        groups_list = ''
        for g in SENGING_GROUPS:
            groups_list += (grps_info[g]['name'] + '\n')
        await message.answer('Список групп для рассылки:\n\n' + groups_list, reply_markup = kb)

async def get_sending_text(message : types.Message):
    await Scheme_position.get_sendind_text.set()
    await message.answer('Введите текст рассылаемого сообщения', reply_markup = ReplyKeyboardRemove())

async def resume_sending(message : types.Message):
    global SENDING_TEXT
    SENDING_TEXT = message.text
    await Scheme_position.admin_mode.set()
    resp = await api_requests.get_groups_info(message.from_user.id)
    grps_info = resp['groups']
    if 'all' in SENGING_GROUPS: groups_list = 'По всем пользователям\n'
    else:
        groups_list = ''
        for g in SENGING_GROUPS:
            groups_list += (grps_info[g]['name'] + '\n')
    if SENDING_MODE == 'now': sched_time = '\nСейчас'
    if SENDING_MODE == 'later': sched_time = '\n' + str(SCHEDULE_TIME[0]) + '.' + str(SCHEDULE_TIME[1]) + '.' + str(SCHEDULE_TIME[2]) + ' в ' + str(SCHEDULE_TIME[3]) + ':' + str(SCHEDULE_TIME[4])
    kb = await admin_kb.make_list_kb(CREATE_SENDING_BUTTON_TEXT)
    await message.answer('Рассылка будет произведена по следующим спискам:\n\n' + groups_list + sched_time, reply_markup = kb)

async def create_sending(message : types.Message):
    
    sending_data = {
        'groups':SENGING_GROUPS,
        'text':SENDING_TEXT
    }
    
    if SENDING_MODE == 'now': time = 'now'  
    if SENDING_MODE == 'later': time = SCHEDULE_TIME
       
    resp = await api_requests.get_groups_info(message.from_user.id)
    grps_info = resp['groups']
    if 'all' in SENGING_GROUPS: groups_list = 'По всем пользователям'
    else:
        groups_list = ''
        for g in SENGING_GROUPS:
            groups_list += (grps_info[g]['name'] + ' / ')
    cont = {
        'usr_id':message.from_user.id,
        'text':SENDING_TEXT,
        'time':time,
        'groups':groups_list
    }
    resp = await api_requests.create_sending(cont)
    if resp['status'] == 'OK':
        sending_data.update({'sending_id':resp['sending']})
        kb = await other_kb.create_keyboard('admin_menu', message.from_user.id)
        await message.answer('Рассылка успешно создана!', reply_markup = kb)

        if SENDING_MODE == 'now':
            resp = await sending.send_messages(message.from_user.id, sending_data)
            if resp['status'] == 'OK': 
                await asyncio.sleep(2)
                await message.answer('Рассылка прошла успешно!')
        
        if SENDING_MODE == 'later':
            resp = await run_at(SCHEDULE_TIME, sending.send_messages(message.from_user.id, sending_data), message)
            if resp['status'] == 'OK': 
                await asyncio.sleep(2)
        
    else: await message.answer('Не удалось создать рассылку', reply_markup = ReplyKeyboardRemove())



# Регистрация хендлеров
async def register_handlers_client(dp : Dispatcher):
    initializators = await api_requests.get_content_proxy('RUS', 'kb_buttons')

    dp.register_message_handler(admin_cpanel, Text(equals = initializators['admin_menu']['admin_panel'][0]), state = Scheme_position.admin_mode)
    dp.register_message_handler(get_sending_text, Text(equals = LIST_CONFORM_BUTTON_TEXT), state = Scheme_position.admin_mode)
    dp.register_message_handler(group_choise, Text(equals = LIST_CONFORM_BUTTON_TEXT), state = Scheme_position.set_schedule_time)
    dp.register_message_handler(sendings, Text(equals = initializators['admin_menu']['sendings'][0]), state = Scheme_position.admin_mode)
    dp.register_message_handler(group_choise, Text(equals = initializators['sendings_kb']['right_now'][0]), state = Scheme_position.admin_mode)
    dp.register_message_handler(set_schedule, Text(equals = initializators['sendings_kb']['schedule_message'][0]), state = Scheme_position.admin_mode)
    dp.register_message_handler(sendings, Text(equals = 'Назад'), state = Scheme_position.admin_mode)
    dp.register_message_handler(make_list_result, Text(equals = MAKE_LIST_BUTTON_TEXT), state = Scheme_position.admin_mode)
    dp.register_message_handler(create_sending, Text(equals = CREATE_SENDING_BUTTON_TEXT), state = Scheme_position.admin_mode)
    dp.register_callback_query_handler(get_sending_groups, state = Scheme_position.admin_mode)
    dp.register_message_handler(get_sending_time, state = Scheme_position.set_schedule_time)
    dp.register_message_handler(resume_sending, state = Scheme_position.get_sendind_text)
    