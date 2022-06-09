from components import api_connector
import asyncio, logging, requests
import subprocess
from sys import argv
from flask import Flask, request


RUNNING_BOTS = {'status':'OK'}
BOT_INIT_SCRIPT = '/var/www/dev.insiderlab.ru/bot_controller_sm/components/bot_starter.py'

bots_names = []
active_bots_names = []
auth_token = None

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'AES_vj5knSDfvknLa5sdflTkn3cvjFnsadlf7Dkjhbasc2Dha6dWf4nbhj8Cbs3dhb'

async def start_bots(bots_names: list, auth_token):
    global RUNNING_BOTS
    for bot_name in bots_names:
        bot_info = await api_connector.AsyncGetBotInfo(bot_name, auth_token)
        api_token = bot_info[bot_name]['token']

        # запуск бота
        bot_process = subprocess.Popen(['python', BOT_INIT_SCRIPT, api_token, auth_token, bot_name])
        RUNNING_BOTS.update({bot_name:bot_process})

        await asyncio.sleep(2)
        print(f'{bot_name} started')

async def stop_bots(bots_names: list):
    global RUNNING_BOTS
    for bot_name in bots_names:

        # остановка бота
        bot_process = RUNNING_BOTS[bot_name]
        bot_process.terminate()
        print(f'{bot_name} stoped')

@app.route('/', methods = ('GET', 'POST'))
async def bots_control():
    global active_bots_names
    global auth_token
    if request.method == "POST":
        action = request.json['action']
        bot_name = request.json['bot_name']
        bots = []
        match action:
            case 'add': 
                if bot_name not in active_bots_names: 
                    active_bots_names.append(bot_name)
                    bots.append(bot_name)
                    await asyncio.create_task(start_bots(bots, auth_token))
            case 'remove': 
                if bot_name in active_bots_names:
                    active_bots_names.extend(bot_name)
                    bots.append(bot_name)
                    await asyncio.create_task(stop_bots(bots))
    return bot_name

async def main(bots_info, AT):
    global bots_names
    global active_bots_names
    global auth_token

    auth_token = AT

    for k in bots_info.keys():
        if k != 'status':
            if bots_info[k]['active'] == True:
                active_bots_names.append(k)

    data = {}
    changes = {'added':'', 'removed':''}
    if active_bots_names != bots_names:
        changes.update({'added':list(set(active_bots_names) - set(bots_names))})
        bots_names = active_bots_names
        data.update({
            'msg':'bots list updated',
            'Added':str(changes['added'])
        })
        await asyncio.create_task(start_bots(changes['added'], auth_token))
        print(str(data))
    asyncio.create_task(app.run())
    print(RUNNING_BOTS)
    return None

if __name__ == '__main__':

    try:
        login = argv[1]
        passwd = argv[2]
    except: 
        login = None
        passwd = None
    
    server_host = 'https://' + api_connector.SERVER_HOST + '/auth/token'
    while True:
        resp = requests.post(server_host, json = {"username":login, "password":passwd, "grant_type":"password"})
        try: 
            resp.json()['token_type'] == 'Bearer'
            break
        except:
            login = input('Enter login: ')
            passwd = input('Enter password: ')

    auth_token = resp.json()['access_token']
    logging.basicConfig(level = logging.INFO)

    bots_info = api_connector.GetBotInfo('all', auth_token)
    asyncio.run(main(bots_info, auth_token))
