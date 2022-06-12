from bot_init import WEBHOOK_URL_PATH, on_startup, on_shutdown, WEBAPP_HOST, WEBAPP_PORT
from bot_dispatcher import dp
from aiogram.utils.executor import start_webhook

import logging

logging.basicConfig(level = logging.INFO)

#other.register_handlers_other(dp)
#admin.register_handlers_other(dp)
#client.register_handlers_other(dp)
#partner.register_handlers_other(dp)

if __name__ == '__main__':
    start_webhook(
        dispatcher = dp,
        webhook_path = WEBHOOK_URL_PATH,
        on_startup = on_startup,
        on_shutdown = on_shutdown,
        skip_updates = True,
        host = WEBAPP_HOST,
        port = WEBAPP_PORT
    )