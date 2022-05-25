from aiogram import Dispatcher, types
from api_connector import GetContent, AsyncGetContent, AsyncAddUser, AsyncGetUserInfo
from keyboard_creator import create_keyboard
from aiogram.types import ReplyKeyboardRemove

AT = None
BN = None

def MakeCommandList(auth_token, bot_name):
    commands_info = GetContent(bot_name, auth_token, 'commands')['commands']
    commands_list = []
    for k in commands_info.keys():
        commands_list.append(k)
    return commands_list

async def command_react(message : types.Message):
    global AT, BN
    commands_info = GetContent(BN, AT, 'commands')
    cmd = message.text.replace('/','').split(' ')[0]
    text = commands_info['commands'][cmd]['text']
    kb = ReplyKeyboardRemove()
    if commands_info['commands'][cmd]['keyboard'] != 'null': kb = await create_keyboard(BN, AT, commands_info['commands'][cmd]['keyboard'], message.from_user.id)
    if cmd == 'start':
        resp_api = await AsyncGetUserInfo(BN, AT, message.from_user.id)
        if resp_api['status'] == 'error':
            if len(message.text) > 6:
                USER_TAG = message.text.split()[1]
                data = {
                    "usr_id": message.from_user.id,
                    "teleg": message.from_user.username,
                    "usr_name": f'{message.from_user.first_name} {message.from_user.last_name}',
                    "usr_tag": USER_TAG
                }
                resp = await AsyncAddUser(BN, AT, data)
                await message.answer(str(resp))
    await message.answer(text, reply_markup = kb)

def register_message_handlers(dp:Dispatcher, auth_token, bot_name):
    global AT, BN
    AT = auth_token
    BN = bot_name
    commands_list = MakeCommandList(auth_token, bot_name)
    
    dp.register_message_handler(command_react, commands = commands_list)