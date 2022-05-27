import aiohttp, requests

SERVER_HOST = 'dev.insiderlab.ru'

def GetContent(bot_name, auth_token, target):
    head = {'Authorization': 'Bearer ' + auth_token, 'Content-Type':'application/json'}
    PATH = '/content/'
    SERVER_URL = 'https://' + SERVER_HOST + PATH
    data = {
        'botname':bot_name,
        'head':target,
        'block':''
    }
    resp_api = requests.get(SERVER_URL, params = data, headers = head)
    return resp_api.json()

async def AsyncGetContent(bot_name, auth_token, target):
    head = {'Authorization': 'Bearer ' + auth_token, 'Content-Type':'application/json'}
    PATH = '/content/'
    SERVER_URL = 'https://' + SERVER_HOST + PATH
    if type(target) == str:
        data = {
            'botname':bot_name,
            'head':target,
            'block':''
        }
    elif type(target) == list:
        data = {
            'botname':bot_name,
            'head':target[0],
            'block':target[1]
        }
    async with aiohttp.ClientSession(headers = head) as session:
        async with session.get(SERVER_URL, params = data) as resp:
            response = resp.json()
            return response

def GetBotInfo(bot_name : str, auth_token):
    PATH = '/API_v1/bot/'
    SERVER_URL = 'https://' + SERVER_HOST + PATH
    head = {'Authorization': 'Bearer ' + auth_token}
    resp_api = requests.get(SERVER_URL, params = {'bot_name':bot_name}, headers = head)
    return resp_api.json()

async def AsyncGetBotInfo(bot_name : str, auth_token):
    PATH = '/API_v1/bot/'
    SERVER_URL = 'https://' + SERVER_HOST + PATH
    head = {'Authorization': 'Bearer ' + auth_token}
    async with aiohttp.ClientSession(headers = head) as session:
        async with session.get(SERVER_URL, params = {'bot_name':bot_name}) as resp:
            response = await resp.json()
            return response

async def AsyncAddUser(bot_name, auth_token, data):
    PATH = '/users_api/new_user/'
    SERVER_URL = 'https://' + SERVER_HOST + PATH
    head = {'Authorization': 'Bearer ' + auth_token}
    push_params = {
        'bot_name':bot_name,
        'head':'new_user_start',
        'usr_id':data['usr_id'],
        'teleg':data['teleg'],
        'usr_name':data['usr_name'],
        'usr_tag':data['usr_tag']
    }
    async with aiohttp.ClientSession(headers = head) as session:
        async with session.post(SERVER_URL, json = push_params) as resp:
            response = await resp.json()
            return response
        
async def AsyncGetUserInfo(bot_name, auth_token, user_id, target):
    PATH = '/users_api/get_user/'
    SERVER_URL = 'https://' + SERVER_HOST + PATH
    head = {'Authorization': 'Bearer ' + auth_token}
    data = {
        'head':target,
        'user_id':user_id
    }
    async with aiohttp.ClientSession(headers = head) as session:
        async with session.get(SERVER_URL, params = data) as resp:
            response = await resp.json()
            return response