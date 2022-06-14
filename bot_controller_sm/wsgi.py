from components import api_connector
import asyncio, logging, requests
import subprocess, os, redis, signal
from flask import Flask, request

red_env = redis.Redis(host = "localhost", port = 6379, charset = "utf-8", decode_responses = True)
bots_names = []
active_bots_names = []
auth_token = None
env = os.environ
bots_not_running = True

async def start_bots(bots_names: list, auth_token):
    print('START BOTS')
    for bot_name in bots_names:
        bot_info = await api_connector.AsyncGetBotInfo(bot_name, auth_token)
        api_token = bot_info[bot_name]['token']

        # запуск бота
        script_path = env['PROJ_PATH'] + '/bot_controller_sm/components/bot_starter.py'
        bot_process = subprocess.Popen(['python', script_path, api_token, auth_token, bot_name])
        print(bot_process.pid)
        red_env.mset({bot_name:bot_process.pid})
        
        await asyncio.sleep(2)
        print(f'{bot_name} started')

async def stop_bots(bots_names: list):
    print('STOP BOTS')
    for bot_name in bots_names:

        # остановка бота
        os.kill(int(red_env.get(bot_name)), signal.SIGKILL)
        red_env.set(bot_name, 'inactive')
        
        print(f'{bot_name} stoped')

async def main(bots_info, AT):
    print('STARTS MAIN')

    global bots_names, active_bots_names, auth_token, bots_not_running

    auth_token = AT

    changes = {'added':'', 'removed':''}
    counter = 0
    for k in bots_info.keys():
        if k != 'status':
            red_env.set(k, 'inactive')
            if bots_info[k]['active'] == True:
                active_bots_names.append(k)
                red_env.set(k, 'active')
                counter += 1
    changes.update({'added':active_bots_names})

    if counter > 0:
        await asyncio.create_task(start_bots(changes['added'], auth_token))
        print('Starting' + str(changes['added']))
    bots_not_running = False
    # asyncio.create_task(app.run())
    print('END MAIN')
    # return None

def application():
    print('STARTS APP')
    global bots_not_running
    try:
        login = env['AUTH_NAME']
        passwd = env['AUTH_PASS']
        print('ENV OK')
    except: 
        login = None
        passwd = None
    
    server_host = 'https://' + api_connector.SERVER_HOST + '/auth/token'
    if bots_not_running:
        print('BOTS NOT RUNNING')
        while True:
            resp = requests.post(server_host, json = {"username":login, "password":passwd, "grant_type":"password"})
            try: 
                resp.json()['token_type'] == 'Bearer'
                break
            except: raise EnvironmentError

        auth_token = resp.json()['access_token']
        logging.basicConfig(level = logging.INFO)

        bots_info = api_connector.GetBotInfo('all', auth_token)
        asyncio.run(main(bots_info, auth_token))
    print('END APP')
        
app = Flask(__name__)
app.ensure_sync(application)()

@app.route('/', methods = ('GET', 'POST'))
async def bots_control():
    print('RECIVE')
    global auth_token
    if request.method == "POST":
        print('POST')
        action = request.json['action']
        bot_name = request.json['bot_name']
        bots = []
        match action:
            case 'add':
                print('ADD')
                print(bot_name)
                if red_env.get(bot_name) == 'inactive': 
                    bots.append(bot_name)
                    await asyncio.create_task(start_bots(bots, auth_token))
            case 'remove':
                print('RM')
                print(bot_name)
                if red_env.get(bot_name) != 'inactive':
                    bots.append(bot_name)
                    await asyncio.create_task(stop_bots(bots))
    return bot_name

if __name__ == '__main__':
    start = application()