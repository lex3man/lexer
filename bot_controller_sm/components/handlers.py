from aiogram import Dispatcher, types

async def start_cmd(message : types.Message):
    await message.answer('OK')

def register_message_handlers(dp:Dispatcher, auth_token):
    
    dp.register_message_handler(start_cmd, commands = ['start', 'help'])