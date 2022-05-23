from components import api_connector
import asyncio, logging, requests
import subprocess

RUNNING_BOTS = {'status':'OK'}
BOT_INIT_SCRIPT = '/var/www/dev.insiderlab.ru/bot_controller_sm/components/bot_starter.py'

async def start_bots(bots_names: list, auth_token):
    global RUNNING_BOTS
    for bot_name in bots_names:
        bot_info = await api_connector.AsyncGetBotInfo(bot_name, auth_token)
        api_token = bot_info[bot_name]['token']
        
        # запуск бота
        bot_process = subprocess.Popen(['python', BOT_INIT_SCRIPT, api_token, auth_token])
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

async def main(auth_token):
    bots_names = []
    while True:
        bots_info = await api_connector.AsyncGetBotInfo('all', auth_token)
        active_bots_names = []
        changes = {'added':'', 'removed':''}
        for k in bots_info.keys():
            if k != 'status':
                if bots_info[k]['active'] == True: 
                    active_bots_names.append(k)
        if active_bots_names != bots_names:
            if len(bots_names) < len(active_bots_names): changes.update({'added':list(set(active_bots_names) - set(bots_names))})
            else: changes.update({'removed':list(set(bots_names) - set(active_bots_names))})
            bots_names = active_bots_names
            print('bots list updated')
            if changes['added'] != '':
                asyncio.create_task(start_bots(changes['added'], auth_token))
                print('Added ' + str(changes['added']))
            if changes['removed'] != '':
                asyncio.create_task(stop_bots(changes['removed']))
                print('Removed ' + str(changes['removed']))

if __name__ == '__main__':
    login = 'lex3man'
    while True:
        passwd = input('Enter password: ')
        resp = requests.post('https://dev.insiderlab.ru/auth/token', json = {"username":login, "password":passwd, "grant_type":"password"})
        try: 
            resp.json()['token_type'] == 'Bearer'
            print('Service started...')
            break
        except: pass
    
    auth_token = resp.json()['access_token']
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main(auth_token))