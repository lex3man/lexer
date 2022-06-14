
import aiohttp, json

# Запрос на RSI API

async def request_rsi(data):
    url = 'https://api.rsi.wocom.biz/tg1'
    pref = data['pref']
    rsi_id = data['id']
    auth_token = '$zZ*ikCvz8DT5QI7T7*yBv0kbnFsz*Bz6oD09nb86zWTrlZbHRtvvPqRk@*i%%zI'
    head = {'Authorization': 'Bearer ' + auth_token}
    async with aiohttp.ClientSession(headers = head) as session:
        async with session.get(url + pref, params = {"id":rsi_id}) as resp:
            response = await resp.json()
            return(response)

# Запрос к базе данных пользователей

SERVER_URL = 'https://lexer.insiderlab.ru/'

async def get_usr_info(usr_id):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/get_info/', json = {'usr_id':usr_id, 'head':'user_info'}) as resp:
            response = await resp.json()
            return(response)

async def get_groups_info(usr_id):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/get_info/', json = {'usr_id':usr_id, 'head':'groups_info'}) as resp:
            response = await resp.json()
            return(response)

async def get_group_users_info(usr_id, group_name):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/get_info/', json = {'usr_id':usr_id, 'group':group_name, 'head':'group_members'}) as resp:
            response = await resp.json()
            return(response)

async def get_part_info(usr_id):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/get_info/', json = {'usr_id':usr_id, 'head':'part_info'}) as resp:
            response = await resp.json()
            return(response)   

async def edit_usr_info(data):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/get_info/', json = data) as resp:
            response = await resp.json()
            return(response)

async def reg_usr(data):
    global SERVER_URL
    data.update({'head':'new_user'})
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/updates/', json = data) as resp:
            response = await resp.json()
            return(response) 

# Запись истории сообщений

async def history_record(usr_id, text):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'msg_log/updates/', json = {'usr_id':usr_id, 'text':text}) as resp:
            response = await resp.json()
            return(response)

# Создание рассылки

async def create_sending(data):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'msg_log/create_sending/', json = data) as resp:
            response = await resp.json()
            return(response)

async def sent(sending, report_usrs):
    report = {'sending':sending, 'usrs':report_usrs}
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'msg_log/sent/', json = report) as resp:
            response = await resp.json()
            return(response)

# Отправка вводимых данных

async def data_send(stack):
    global SERVER_URL
    data = {'head':'upcoming_data', 'stack':stack}
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/updates/', json = data) as resp:
            response = await resp.json()
            return(response)

# Запрос языкового контента для ответов бота

async def get_bot_content(lang, state):
    global SERVER_URL
    async with aiohttp.ClientSession() as session:
        if type(state) == str:
            async with session.get(SERVER_URL + 'bot_content/api/', params = {'lang':lang, 'state':state}) as resp:
                response = await resp.json()
                return(response)
        if type(state) == list:
            async with session.get(SERVER_URL + 'bot_content/api/', params = {'lang':lang, 'state':state[0], 'additional':state[1], 'user_id':state[2]}) as resp:
                response = await resp.json()
                return(response)

async def get_content_proxy(lang, state):
    if type(state) == str: get_file = './content_swap/' + lang + '/' + state + '.json'
    if type(state) == list: get_file = './content_swap/' + lang + '/' + state[0] + '.json'
    resp_api = await get_bot_content(lang, state)
    try:
        resp_api = await get_bot_content(lang, state)
        if resp_api['status'] == 'OK':
            with open(get_file, "w") as f:
                json.dump(resp_api, f)
                f.close()
            if type(state) == str: content = resp_api[state]
            if type(state) == list: content = resp_api[state[0]]
    except:
        with open(get_file, "r") as f:
            json_body = json.loads(f.read())
            f.close()
        if type(state) == str: content = resp_api[state]
        if type(state) == list: content = resp_api[state[0]]
    return content