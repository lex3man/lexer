from django.http import JsonResponse
from django.views import View
from datetime import datetime
from .models import message_history, sendings
from webhook.models import User, Bot_config

import random, string, json

class MessageLogging(View):
    def post(self, request):
        post_body = json.loads(request.body)
        
        usr_id = post_body.get('usr_id')
        bot_id = 'rsi_business_bot'
        get_msg_text = post_body.get('text')
        
        data = {'status':'OK'}
        try:
            guser = User.objects.get(tg_ID = usr_id)
            gbot = Bot_config.objects.get(bot_name = bot_id)
            new_record = message_history(
                date_time = datetime.now(),
                bot = gbot,
                user = guser,
                msg_text = get_msg_text
            )
            new_record.save()
            
            data.update({'msg':'Записал'})
        except: data.update({'msg':'Пользователь не представился'})
        
        return JsonResponse(data)
    
class CreateSending(View):
    def post(self, request):
        post_body = json.loads(request.body)
        
        usr_id = post_body.get('usr_id')
        get_sending_text = post_body.get('text')
        get_sending_time = post_body.get('time')
        get_sending_groups = post_body.get('groups')
        if get_sending_time == 'now': sending_time = datetime.now()
        else: 
            year = int(get_sending_time[2])
            month = int(get_sending_time[1])
            day = int(get_sending_time[0])
            hours = int(get_sending_time[3])
            minuts = int(get_sending_time[4])
            sending_time = datetime(year, month, day, hours, minuts, 0, 0)
        
        data = {'status':'OK'}
        try:
            guser = User.objects.get(tg_ID = usr_id)
            while True:
                code = ''.join(random.choices(string.ascii_lowercase, k = 9))
                if sendings.objects.filter(sending_id = code).count() == 0:
                    break
            new_sending = sendings(
                sending_id = code,
                creator = guser,
                sending_list = get_sending_groups,
                sending_time = sending_time,
                sending_text = get_sending_text
            )
            new_sending.save()
            
            try:
                if get_sending_time != 'now':
                    
                    pass
            except:
                pass
            
            data.update({'sending':code})
        except: data.update({'msg':'error'})
        
        return JsonResponse(data)

class SendingSend(View):
    def get(self, request):
        data = {}
        sendings_info = sendings.objects.all()
        for sending in sendings_info:
            data.update({
                sending.sending_id:{
                    'groups_list':sending.sending_list, 
                    'sending_time':sending.sending_time, 
                    'sending_text':sending.sending_text
                    }
                })
        return JsonResponse(data)

    def post(self, request):
        post_body = json.loads(request.body)
        sending = post_body.get('sending')
        usrs = post_body.get('usrs')
        get_sending = sendings.objects.get(sending_id = sending)
        text = 'Попытка рассылки по ' + str(len(usrs)) + ' пользователям\n\n'
        data = {'status': 'OK'}
        count = 0
        for tg_id in usrs.keys():
            user = User.objects.get(tg_ID = tg_id)
            user.ping_stat = False
            user.save()
            if usrs[tg_id]: 
                user.set_active()
                count += 1
        text += 'Доставленно ' + str(count) + ' сообщений\n\n'
        for tg_id in usrs.keys():
            user = User.objects.get(tg_ID = tg_id)
            text += user.name + ' (' + user.tg_nickname + '): ' + str(usrs[tg_id]) + '\n'
        get_sending.report = text
        get_sending.sending_done()
        
        return JsonResponse(data)
        