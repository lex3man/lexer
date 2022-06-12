from bot_dispatcher import bot
from mods import api_requests

async def send_messages(usr_id, data):
    groups = data['groups']
    if 'all' in groups: groups = ['all']
    users_id = []
    for group_name in groups:
        resp = await api_requests.get_group_users_info(usr_id, group_name)
        users_info = resp['users']
        tg_ids = users_info.keys()
        for i in tg_ids:
            users_id.append(i)

    # await bot.send_message(*users_id, data['text'])
    report = {}
    for usr_id in users_id:
        try:
            await bot.send_message(usr_id, data['text'])
            report.update({usr_id:True})
        except: report.update({usr_id:False})
    
    resp_data = {'status':'OK', 'usrs':report}
    sending_id = data['sending_id']
    await api_requests.sent(sending_id, report)
    
    return resp_data