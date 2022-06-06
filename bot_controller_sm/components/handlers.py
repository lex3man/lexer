from aiogram import Dispatcher, types
from api_connector import GetContent, AsyncGetContent, AsyncAddUser, AsyncGetUserInfo
from keyboard_creator import create_keyboard
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from time import sleep

AT = None # Auth API-token
BN = None # Bot name
NB = None # Next block ID

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

async def ConditionsMatch(conditions_info, user_info, user_vars):
    user_tags_list = user_info['tags']
    user_vars_dict = user_vars['vars']
    response = {
        'condition':'all',
        'qual':'dismatch'
    }
    if conditions_info != {}:
        
        for condition_key in conditions_info.keys():
            if conditions_info[condition_key]['usr_tag'] != 'None':
                response.update({'condition':'tag', 'qual':'dismatch'})
                if conditions_info[condition_key]['usr_tag'] in user_tags_list: 
                    response.update({'qual':'match', 'condition_key':condition_key})
                    return response
            else:
                response.update({'condition':'var', 'qual':'dismatch'})
                quality = conditions_info[condition_key]['qual']
                var_usr = conditions_info[condition_key]['var_key']
                var_cond = conditions_info[condition_key]['var_value']
                match quality:
                    case '=': 
                        if user_vars_dict[var_usr] == var_cond:
                            response.update({'qual':'match'})
                            return response
                    case '>=':
                        if int(user_vars_dict[var_usr]) >= int(var_cond):
                            response.update({'qual':'match'})
                            return response
                    case '>':
                        if int(user_vars_dict[var_usr]) > int(var_cond):
                            response.update({'qual':'match'})
                            return response
                    case '<=':
                        if int(user_vars_dict[var_usr]) <= int(var_cond):
                            response.update({'qual':'match'})
                            return response
                    case '<':
                        if int(user_vars_dict[var_usr]) < int(var_cond):
                            response.update({'qual':'match'})
                            return response
    return response


# Обработчик БЛОКА СООБЩЕНИЙ бота
async def content_block(message : types.Message, *args):
    global AT, BN, NB
    if args[0] == 1:
        resp_api_blck = await AsyncGetContent(BN, AT, ['blocks', NB])
        resp_api_usr = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'user')
        resp_api_vrs = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'vars')
        text = resp_api_blck['blocks'][NB]['text']
        delay = int(resp_api_blck['blocks'][NB]['delay'])
        kb_name = resp_api_blck['blocks'][NB]['keyboard']
        kb = ReplyKeyboardRemove()
        if kb_name != 'null': kb = await create_keyboard(BN, AT, kb_name, message.from_user.id)

        conditions_info = resp_api_blck['blocks'][NB]['conditions']
        if conditions_info == {}:
            sleep(delay)
            await message.answer(text, reply_markup = kb)
            NB = None
            if kb_name == 'null': NB = resp_api_blck['blocks'][NB]['next_block']
        else:
            condition_match = await ConditionsMatch(conditions_info, resp_api_usr[str(message.from_user.id)], resp_api_vrs)
            if condition_match['qual'] == 'match':
                sleep(delay)
                await message.answer(text, reply_markup = kb)
                NB = None
                if kb_name == 'null': NB = resp_api_blck['blocks'][NB]['next_block']

# Обработчик КОМАНД боту
async def command_react(message : types.Message):
    global AT, BN, NB
    cmd = message.text.replace('/','').split(' ')[0]
    commands_info = await AsyncGetContent(BN, AT, 'commands')
    text = commands_info['commands'][cmd]['text']
    kb = ReplyKeyboardRemove()
    resp_api_usr = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'user')
    if commands_info['commands'][cmd]['keyboard'] == 'null': kb = ReplyKeyboardRemove()
    else: kb = await create_keyboard(BN, AT, commands_info['commands'][cmd]['keyboard'], message.from_user.id)
    if cmd == 'start':
        if resp_api_usr['status'] != 'OK':
            USER_TAG = ''
            if len(message.text) > 6: USER_TAG = message.text.split()[1]
            data = {
                "usr_id": message.from_user.id,
                "teleg": message.from_user.username,
                "usr_name": f'{message.from_user.first_name} {message.from_user.last_name}',
                "usr_tag": USER_TAG
            }
            resp = await AsyncAddUser(BN, AT, data)
            
            # !!!Сюда надо добавить ответ при первом касании из админки (в админку добавить поле для ответа на первое касание)!!!
            text = commands_info['first_touch']['text']
            if commands_info['first_touch']['keyboard'] == 'null': kb = ReplyKeyboardRemove()
            else: kb = await create_keyboard(BN, AT, commands_info['first_touch']['keyboard'], message.from_user.id)
            await message.answer(text, reply_markup = kb)
    
    resp_api_vrs = await AsyncGetUserInfo(BN, AT, message.from_user.id, 'vars')
    if resp_api_usr['status'] == 'OK':
        usr_info = resp_api_usr[str(message.from_user.id)]
        
        # Проверка условий выполнения команды
        conditions_info = commands_info['conditions'][cmd]
        if conditions_info == {}:
            await message.answer(text, reply_markup = kb)
            NB = None
            if commands_info['commands'][cmd]['keyboard'] == 'null': NB = commands_info['commands'][cmd]['next_block']
        else:
            condition_match = await ConditionsMatch(conditions_info, usr_info, resp_api_vrs)
            if condition_match['qual'] == 'match':
                await message.answer(text, reply_markup = kb)
                NB = None
                if commands_info['commands'][cmd]['keyboard'] == 'null': NB = commands_info['commands'][cmd]['next_block']
        
        if NB is not None:
            await content_block(message, 1)

def register_message_handlers(dp:Dispatcher, auth_token, bot_name):
    global AT, BN
    AT = auth_token
    BN = bot_name
    commands_list = MakeCommandList(auth_token, bot_name)
    button_list = MakeButtonsList(auth_token, bot_name)
    
    dp.register_message_handler(command_react, commands = commands_list)
    dp.register_message_handler(content_block, Text(equals = button_list, ignore_case = True), state = "*")
from aiogram import Dispatcher, types
