from bot_dispatcher import bot, dp
from aiogram.types import ContentTypes
from aiogram.types import ReplyKeyboardRemove
from aiogram import types
from mods import partner, client, other, api_requests, admin
from keyboards import other_kb

import requests, logging

get_bot = requests.post(api_requests.SERVER_URL + 'config_api/bot_request/', json = {'bot_name':'rsi_business_bot'})

WEBHOOK_HOST = get_bot.json()['WEBHOOK_HOST']
WEBHOOK_PORT = get_bot.json()['WEBHOOK_PORT']
WEBHOOK_URL_PATH = get_bot.json()['WEBHOOK_URL_PATH']

WEBHOOK_SSL_CERT = get_bot.json()['WEBHOOK_SSL_CERT']
WEBHOOK_SSL_PRIV = get_bot.json()['WEBHOOK_SSL_PRIV']

WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"

WEBAPP_HOST = get_bot.json()['WEBAPP_HOST']
WEBAPP_PORT = get_bot.json()['WEBAPP_PORT']

BAD_CONTENT = ContentTypes.PHOTO & ContentTypes.DOCUMENT & ContentTypes.STICKER & ContentTypes.AUDIO

async def on_startup(dp):
    print('Стартуем...')
    await bot.set_webhook(WEBHOOK_URL)
    await admin.register_handlers_client(dp)
    await client.register_handlers_client(dp)
    await partner.register_handlers_admin(dp)
    await other.register_handlers_other(dp)

async def on_shutdown(dp):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')

@dp.message_handler(commands = ['start'])
async def start_message(message : types.Message):
    await api_requests.history_record(message.from_user.id, message.text)
    if len(message.text) > 6:
        other.USER_TAG = message.text.split()[1]
    resp_api = await api_requests.get_usr_info(message.from_user.id)
    if resp_api['status'] == 'OK': other.USER_NAME = resp_api['name'].replace('"','')
    start_content = await api_requests.get_content_proxy("RUS", "start_cont")
    try:
        await bot.send_message(message.from_user.id, start_content['hello_message'], reply_markup = ReplyKeyboardRemove())
        resp_api = await api_requests.get_usr_info(message.from_user.id)
        if resp_api['status'] == 'OK':
            keyboard = await other_kb.create_keyboard('name_verify_kb', message.from_user.id)
            await bot.send_message(message.from_user.id, start_content['name_verify_welcome'] % other.USER_NAME, reply_markup = keyboard)
            await other.Scheme_position.identity.set()
        elif resp_api['status'] == 'error':
            await bot.send_message(message.from_user.id, start_content['get_user_name'])
            await other.User.name.set()
        else:
            await bot.send_message(message.from_user.id, start_content['data_access_error'])
    except:
        await message.answer(start_content['wrong_chat_message'])