from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import User, UserTag
from core.models import TgBot
from datetime import date

from rest_framework import authentication
from bearer_auth.models import AccessToken

import json
import random, string

def get_ref_code():
    while True:
        code = ''.join(random.choices(string.ascii_lowercase, k = 9))
        if User.objects.filter(ref_code = code).count() == 0:
            break
    return code

class CreateUser(View):
    def post(self, request):
        data = {'status':'error'}
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header:
            return JsonResponse(data)
        if len(auth_header) == 1:
            return JsonResponse(data)
        elif len(auth_header) > 2:
            return JsonResponse(data)
        try:
            token = auth_header[1].decode('utf-8')
            AccessToken.objects.get(key = token)
        except: return JsonResponse(data)
        
        json_body = json.loads(request.body)
        head = json_body.get('head')
        
        if head == 'new_user_start':
            get_bot_name = json_body.get('bot_name')
            get_usr_id = json_body.get('usr_id')
            get_usr_tg = json_body.get('teleg')
            get_usr_ref = json_body.get('usr_tag')
            ref_code = 'None'
            pref = get_usr_ref
            if len(get_usr_ref) > 8: 
                ref_code = get_usr_ref
                pref = 'None'
            if len(get_usr_ref) > 10: 
                ref_code = get_usr_ref.split('_')[1]
                pref = get_usr_ref.split('_')[0]
            try:
                default_tag = UserTag.objects.get(tag_id = '001')
                new_user_code = get_ref_code()
                tgbot = TgBot.objects.get(caption = get_bot_name)
                user = User(
                    tg_ID = get_usr_id,
                    name = 'none',
                    tg_nickname = get_usr_tg,
                    registration_date = date.today(),
                    parent_ref_code = ref_code,
                    ref_code = new_user_code,
                    from_bot = tgbot
                )
                user.save()
                user.tags.add(default_tag)
                user.from_bot = tgbot
                data.update({
                    'status':'OK',
                    'msg':'Added new start'
                })
            except: data.update({'status':'error', 'msg':'Не получилось зарегистрировать пользователя'})
        return JsonResponse(data)
        