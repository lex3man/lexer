from aiogram import Dispatcher, types
from api_connector import AsyncSetVar, GetContent, AsyncGetContent, AsyncAddUser, AsyncGetUserInfo
from keyboard_creator import create_keyboard
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from time import sleep

AT = None # Auth API-token
BN = None # Bot name
NB = None # Next block ID
InputMode = False
AutoCall = False
save_to = None

def MakeButtonsList(auth_token, bot_name):
    buttons_info = GetContent(bot_name, auth_token, 'buttons')['buttons']
    buttons_list = []
    for k in buttons_info.keys():
        buttons_list.append(buttons_info[k]['text'])
    return buttons_list

def MakeCommandList(auth_token, bot_name):
    commands_info = GetContent(bot_name, auth_token, 'commands')['commands']
    commands_list = []
    for k in commands_info.keys():
        commands_list.append(k)
    return commands_list

async def TextVarsReplace(raw_text, user_vars):
    get_text = raw_text.split('#{')
    get_vars = []
    for i in range(len(get_text)):
        x = len(get_text) - 1 - i
        var_name = get_text[x].split('}')[0]
        get_vars.append(var_name)
    for v in get_vars:
        try: user_var = user_vars[v]
        except: user_var = 'None'
        replacement = '#{' + v + '}'
        raw_text = raw_text.replace(replacement, user_var)
    text_out = raw_text
    return text_out

async def ConditionsMatch(conditions_info, user_info, user_vars):
    user_tags_list = user_info['tags']
    user_vars_dict = user_vars['vars']
    match_result = False
    for condition_key in conditions_info.keys():
        if conditions_info[condition_key]['usr_tag'] != 'None':
            match_result = True
            if conditions_info[condition_key]['usr_tag'] not in user_tags_list: return False
        else:
            quality = conditions_info[condition_key]['qual']
            var_usr = conditions_info[condition_key]['var_key']
            var_cond = conditions_info[condition_key]['var_value']
            try:
                match quality:
                    case '=':
                        if user_vars_dict[var_usr] == var_cond: match_result = True
                        else: return False
                    case '>=':
                        if float(user_vars_dict[var_usr]) >= float(var_cond): match_result = True
                        else: return False
                    case '>':
                        if float(user_vars_dict[var_usr]) > float(var_cond): match_result = True
                        else: return False
                    case '<=':
                        if float(user_vars_dict[var_usr]) <= float(var_cond): match_result = True
                        else: return False
                    case '<':
                        if float(user_vars_dict[var_usr]) < float(var_cond): match_result = True
                        else: return False
            except: return False
    return match_result

async def UnknownBlock(message : types.Message):
    global AT, BN, NB, InputMode, save_to, AutoCall
    if InputMode:
        InputMode = False
        var_data = {
            'usr_id':message.from_user.id,
            'var_name':save_to,
            'var_value':message.text
        }
        await AsyncSetVar(BN, AT, var_data)
        save_to = None
        await content_block(message)
        return True
    else: await message.answer('Однажды здесь будет ответ искусственного интеллекта', reply_markup = ReplyKeyboardRemove())

# Обработчик БЛОКА СООБЩЕНИЙ бота
async def content_block(message : types.Message):
    global AT, BN, NB, InputMode, save_to, AutoCall
    resp_api_usr = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'user')
    resp_api_vrs = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'vars')
    if AutoCall:
        resp_api_blck = await AsyncGetContent(BN, AT, ['blocks', NB])
        block_data = resp_api_blck['blocks'][NB]
        AutoCall = False
    else:
        resp_api_blck = await AsyncGetContent(BN, AT, ['answer', message.text])
        try:
            block_keys = []
            for bk in resp_api_blck['answer'].keys(): block_keys.append(bk)
            block_key = block_keys[0]
            block_data = resp_api_blck['answer'][block_key]
        except:
            if InputMode:
                InputMode = False
                var_data = {
                    'usr_id':message.from_user.id,
                    'var_name':save_to,
                    'var_value':message.text
                }
                await AsyncSetVar(BN, AT, var_data)
                save_to = None
                await content_block(message)
            else: await message.answer('error')

    # Формирование ответа
    text = await TextVarsReplace(block_data['text'], resp_api_vrs['vars'])
    delay = int(block_data['delay'])
    kb_name = block_data['keyboard']
    get_input = block_data['input_state']
    save_to = block_data['save_to_var']
    value_to_save = block_data['value_to_save']

    kb = ReplyKeyboardRemove()
    if kb_name != 'null': kb = await create_keyboard(BN, AT, kb_name, message.from_user.id)
    block_accessable = False
    conditions_info = block_data['conditions']
    if conditions_info == {}: block_accessable = True
    else:
        condition_match = await ConditionsMatch(conditions_info, resp_api_usr[str(message.from_user.id)], resp_api_vrs)
        if condition_match: block_accessable = True
    if block_accessable:
        sleep(delay)
        await message.answer(text, reply_markup = kb)
        NB = None
        if kb_name == 'null': 
            AutoCall = True
            NB = block_data['next_block']
        if get_input == 'true': 
            NB = block_data['next_block']
            AutoCall = True
            InputMode = True
        if value_to_save != 'null':
            var_data = {
                'usr_id':message.from_user.id,
                'var_name':save_to,
                'var_value':value_to_save
            }
            await AsyncSetVar(BN, AT, var_data)
            save_to = None

# Обработчик КОМАНД боту
async def command_react(message : types.Message):
    global AT, BN, NB, AutoCall, save_to, InputMode
    cmd = message.text.replace('/','').split(' ')[0]
    commands_info = await AsyncGetContent(BN, AT, 'commands')
    resp_api_usr = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'user')
    kb = ReplyKeyboardRemove()
    if commands_info['commands'][cmd]['keyboard'] != 'null': 
        kb = await create_keyboard(BN, AT, commands_info['commands'][cmd]['keyboard'], message.from_user.id)
    
    # Если пользователь есть в базе собеседников
    if resp_api_usr['status'] == 'OK':
        resp_api_vrs = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'vars')
        text = await TextVarsReplace(commands_info['commands'][cmd]['text'], resp_api_vrs['vars'])
        usr_info = resp_api_usr[str(message.from_user.id)]
        
        # Проверка условий выполнения команды
        block_accessable = False
        conditions_info = commands_info['conditions'][cmd]
        if conditions_info == {}: block_accessable = True
        else:
            condition_match = await ConditionsMatch(conditions_info, usr_info, resp_api_vrs)
            if condition_match: block_accessable = True
        if block_accessable:
            await message.answer(text, reply_markup = kb)
            NB = None
            if commands_info['commands'][cmd]['keyboard'] == 'null': 
                AutoCall = True
                NB = commands_info['commands'][cmd]['next_block']
    
    # Если пользователя нет в базе собеседников
    else:
        USER_TAG = ''
        if len(message.text) > 6: USER_TAG = message.text.split()[1]
        data = {
            "usr_id": message.from_user.id,
            "teleg": message.from_user.username,
            "usr_name": f'{message.from_user.first_name} {message.from_user.last_name}',
            "usr_tag": USER_TAG
        }
        await AsyncAddUser(BN, AT, data)
        text = commands_info['first_touch']['text']
        if commands_info['first_touch']['keyboard'] == 'None':
            kb = ReplyKeyboardRemove()
            AutoCall = True
            NB = commands_info['first_touch']['next_block']
        else: kb = await create_keyboard(BN, AT, commands_info['first_touch']['keyboard'], message.from_user.id)
        
        await message.answer(text, reply_markup = kb)
    if AutoCall: await content_block(message)

def register_message_handlers(dp:Dispatcher, auth_token, bot_name):
    global AT, BN
    AT = auth_token
    BN = bot_name
    commands_list = MakeCommandList(auth_token, bot_name)
    button_list = MakeButtonsList(auth_token, bot_name)
    
    dp.register_message_handler(command_react, commands = commands_list)
    dp.register_message_handler(content_block, Text(equals = button_list, ignore_case = True), state = "*")
    dp.register_message_handler(UnknownBlock, state = "*")