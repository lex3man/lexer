from sys import argv
from aiogram import Bot, types, executor, md
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from handlers import register_message_handlers

bot_token = argv[1]
auth_token = argv[2]
bot_name = argv[3]

def on_startup(dp, auth_token, bot_name):
    register_message_handlers(dp, auth_token, bot_name)

def BotInit(token):
    return Bot(token)

def BotDp(token):
    bot = BotInit(token)
    dp = Dispatcher(bot, storage = MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())
    return dp

dp = BotDp(bot_token)

executor.start_polling(dp, skip_updates = True, on_startup = on_startup(dp, auth_token, bot_name))
