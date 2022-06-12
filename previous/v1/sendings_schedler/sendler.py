from datetime import datetime as dt
from ..tgbot.mods.sending import send_messages
import asyncio, aiohttp, json, redis

SERVER_URL = 'https://lexer.insiderlab.ru/'
get_file = './content_swap/temp.json'

async def wait_until(time):
    sched_dt = dt(int(time[2]), int(time[1]), int(time[0]), int(time[3]), int(time[4]), 0, 0)
    send_delay = (sched_dt - dt.now()).total_seconds()
    await asyncio.sleep(send_delay)
    
async def run_at(time, func, msg):
    await msg.answer('Запустится ' + str(time[0]) + '.' + str(time[1]) + '.' + str(time[2]) + ' в ' + str(time[3]) + ':' + str(time[4]) + ' МСК')
    await wait_until(time)
    return await func

async def get_group_users_info(usr_id, group_name):
    async with aiohttp.ClientSession() as session:
        async with session.post(SERVER_URL + 'config_api/get_info/', json = {'usr_id':usr_id, 'group':group_name, 'head':'group_members'}) as resp:
            response = await resp.json()
            return(response)

async def main():
    temp_objects = redis.Redis(db=1)
    while True:
        await asyncio.sleep(3)
        async with aiohttp.ClientSession() as session:
            async with session.get(SERVER_URL + 'msg_log/sent/') as resp:
                response = await resp.json()
                with open(get_file, "w") as f:
                    json.dump(response, f)
                    f.close()
                # c = p = 0
                for key in response.keys():
                    if temp_objects.hgetall(key) == {}:
                        temp_objects.hmset(key, response[key])
                        SCHEDULE_TIME = response[key]['sending_time'].replace('-','.').replace(' ','.').replace(':','.').split('.')
                        sending_data = {
                            'groups':'',
                            'text':''
                        }
                        # resp = await run_at(SCHEDULE_TIME, send_messages('284172276', sending_data), message)
                #         c += 1
                #     if c > p: 
                #         print(temp_objects.hgetall(key))
                #         p = c
                # if c == 0: 
                #     print('No changes')

if __name__ == "__main__":
    asyncio.run(main())