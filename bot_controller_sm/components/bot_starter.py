from sys import argv
from aiogram import Bot, types, executor, md
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from handlers import register_message_handlers

bot_token = argv[1]
auth_token = argv[2]

def BotDp(token):
    bot = Bot(token)
    dp = Dispatcher(bot, storage = MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())
    return dp

dp = BotDp(bot_token)

def on_startup(dp):
    register_message_handlers(dp, auth_token)

executor.start_polling(dp, skip_updates = True, on_startup = on_startup(dp))