from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

def BotDp(token):
    bot = Bot(token)
    dp = Dispatcher(bot, storage = MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())
    return dp

def start_webhook(token, WEBHOOK_URL_PATH):
    start_webhook(
        dispatcher = BotDp(token),
        webhook_path = WEBHOOK_URL_PATH,
        on_startup = on_startup,
        on_shutdown = on_shutdown,
        skip_updates = True,
        host = 'localhost',
        port = 3002
    )