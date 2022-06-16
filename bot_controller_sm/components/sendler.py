from datetime import datetime as dt
from api_connector import msg_logging
import asyncio, redis

async def wait_until(time):
    sched_dt = dt(int(time[2]), int(time[1]), int(time[0]), int(time[3]), int(time[4]), 0, 0)
    send_delay = (sched_dt - dt.now()).total_seconds()
    await asyncio.sleep(send_delay)

async def run_at(time, func, msg):
    await msg.answer('Запустится ' + str(time[0]) + '.' + str(time[1]) + '.' + str(time[2]) + ' в ' + str(time[3]) + ':' + str(time[4]) + ' МСК')
    await wait_until(time)
    return await func

async def main():
    temp_objects = redis.Redis(db=10)
    while True:
        await asyncio.sleep(3)
        await msg_logging(temp_objects)

if __name__ == "__main__":
    asyncio.run(main())