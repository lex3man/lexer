from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

def BotDp(token):
    bot = Bot(token)
    dp = Dispatcher(bot, storage = MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())
    return dp

def start_polling(token, set_loop):
    dp = BotDp(token)
    executor.start_polling(dispatcher = dp, loop = set_loop) 