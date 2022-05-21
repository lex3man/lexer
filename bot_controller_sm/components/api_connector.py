import aiohttp, requests

SERVER_HOST = 'dev.insiderlab.ru'
PATH = '/API_v1/bot/'
SERVER_URL = 'https://' + SERVER_HOST + PATH

auth_token = '9077f1964886be134b018a17a4182c76271206f5'
head = {'Authorization': 'Bearer ' + auth_token}

def GetBotInfo(bot_name : str):
    resp_api = requests.get(SERVER_URL, params = {'bot_name':bot_name}, headers = head)
    return resp_api.json()

async def AsyncGetBotInfo(bot_name : str):
    async with aiohttp.ClientSession(headers = head) as session:
        async with session.get(SERVER_URL, params = {'bot_name':bot_name}) as resp:
            response = await resp.json()
            return response