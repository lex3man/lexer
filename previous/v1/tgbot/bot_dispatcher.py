from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

import requests, logging

get_bot = requests.post('https://lexer.insiderlab.ru/config_api/bot_request/', json = {'bot_name':'rsi_business_bot'})

TOKEN = get_bot.json()['TOKEN']

bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage = MemoryStorage())
dp.middleware.setup(LoggingMiddleware())