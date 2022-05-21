from components import api_connector, bot_starter
import asyncio, logging

async def start_bots(bots_names: list):
    for bot_name in bots_names:
        bot_info = await api_connector.AsyncGetBotInfo(bot_name)
        api_token = bot_info[bot_name]['token']
        
        # запуск бота
        path = '/' + bot_name + '/'
        await bot_starter.start_webhook(api_token, path)

        await asyncio.sleep(1)
        print(f'{bot_name} started')

async def stop_bots(bots_names: list):
    for bot_name in bots_names:
        
        # остановка бота

        print(f'{bot_name} stoped')

async def main():
    bots_names = []
    while True:
        bots_info = await api_connector.AsyncGetBotInfo('all')
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
                asyncio.create_task(start_bots(changes['added']))
                print('Added ' + str(changes['added']))
            if changes['removed'] != '':
                asyncio.create_task(stop_bots(changes['removed']))
                print('Removed ' + str(changes['removed']))

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    asyncio.run(main())