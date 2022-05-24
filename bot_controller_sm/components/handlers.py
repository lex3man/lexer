from aiogram import Dispatcher, types
from api_connector import GetContent, AsyncGetContent
import requests

SERVER_HOST = 'dev.insiderlab.ru'

AT = None
BN = None

def MakeCommandList(auth_token, bot_name):
    commands_info = GetContent(bot_name, auth_token, 'commands')['commands']
    commands_list = []
    for k in commands_info.keys():
        commands_list.append(k)
    return commands_list

async def command_react(message : types.Message, *args, **kwargs):
    global AT, BN
    commands_info = GetContent(BN, AT, 'commands')
    cmd = message.text.replace('/','')
    text = commands_info['commands'][cmd]['text']
    await message.answer(text)

def register_message_handlers(dp:Dispatcher, auth_token, bot_name):
    global AT, BN
    AT = auth_token
    BN = bot_name
    commands_list = MakeCommandList(auth_token, bot_name)
    
    dp.register_message_handler(command_react, commands = commands_list)