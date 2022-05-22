import aiohttp, requests

SERVER_HOST = 'dev.insiderlab.ru'
PATH = '/API_v1/bot/'
SERVER_URL = 'https://' + SERVER_HOST + PATH

def GetBotInfo(bot_name : str, auth_token):
    head = {'Authorization': 'Bearer ' + auth_token}
    resp_api = requests.get(SERVER_URL, params = {'bot_name':bot_name}, headers = head)
    return resp_api.json()

async def AsyncGetBotInfo(bot_name : str, auth_token):
    head = {'Authorization': 'Bearer ' + auth_token}
    async with aiohttp.ClientSession(headers = head) as session:
        async with session.get(SERVER_URL, params = {'bot_name':bot_name}) as resp:
            response = await resp.json()
            return response