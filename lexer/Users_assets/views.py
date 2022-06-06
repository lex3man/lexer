from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .models import User, UserTag, RefLink, Var
from core.models import TgBot
from datetime import date, datetime
from django.forms.models import model_to_dict

from rest_framework import authentication
from core.views import auth_check

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
        data = {
            'status':'error',
            'msg':'auth faild'
        }
        
        if auth_check(authentication.get_authorization_header(request).split()) == False: return JsonResponse(data)
        
        data.update({"msg":"Can't create user"})
        json_body = json.loads(request.body)
        head = json_body.get('head')
        
        if head == 'new_user_start':
            get_bot_name = json_body.get('bot_name')
            get_usr_id = json_body.get('usr_id')
            get_usr_tg = json_body.get('teleg')
            get_usr_ref = json_body.get('usr_tag')
            get_usr_name = json_body.get('usr_name')
            ref_code = 'None'
            pref = get_usr_ref
            if len(get_usr_ref) > 8:
                ref_code = get_usr_ref
                pref = 'None'
            if len(get_usr_ref) > 10: 
                ref_code = get_usr_ref.split('_')[1]
                pref = get_usr_ref.split('_')[0]
            try:
                default_tag = UserTag.objects.get(tag_id = 'first_touch')
                new_user_code = get_ref_code()
                tgbot = TgBot.objects.get(caption = get_bot_name)
                user = User(
                    user_ID = new_user_code,
                    tg_ID = get_usr_id,
                    name = get_usr_name,
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
                    'msg':'Added new start',
                    'prefix':pref,
                    'ref':'None'
                })
                if pref != 'None':
                    new_var = Var(
                        user = user,
                        key = 'pref',
                        value = pref
                    )
                    new_var.save()
                if ref_code != 'None':
                    try:
                        parent = User.objects.get(ref_code = ref_code)
                        new_ref = RefLink(
                            caption = parent.name + ' / ' + user.name,
                            date = datetime.now(),
                            parent = parent,
                            child = user
                        )
                        new_ref.save()
                        data.update({'ref':new_ref.caption})
                    except: data.update({'ref':'Error'})
            except: data.update({'status':'error', 'msg':'Не получилось зарегистрировать пользователя'})
        return JsonResponse(data)
    
    def get(self, request):
        data = {
            'status':'error',
            'msg':'auth faild'
        }
        if auth_check(authentication.get_authorization_header(request).split()) == False: return JsonResponse(data)
        
        data.update({'msg':'no matchings'})
        head = request.GET.get('head')
        
        match head:
            case 'user': 
                user_id = request.GET.get('user_id')
                try: 
                    user = User.objects.get(tg_ID = user_id)
                    info = model_to_dict(user, fields = [field.name for field in user._meta.fields])
                    info.update({'from_bot':user.from_bot.caption})
                    info.update({'tags':[tag.tag_id for tag in user.tags.all()]})
                    data.update({
                        'status':'OK',
                        'msg':'Done',
                        user.tg_ID:info
                    })
                except: pass
            case 'vars':
                user_id = request.GET.get('user_id')
                try: 
                    usr = User.objects.get(tg_ID = user_id)
                    usr_vars = Var.objects.filter(user = usr)
                    vars_info = {}
                    for var in usr_vars:
                        vars_info.update({var.key:var.value})
                    data.update({
                        'status':'OK',
                        'msg':'Done',
                        'vars':vars_info
                    })
                except: pass
        return JsonResponse(data)