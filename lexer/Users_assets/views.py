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
        if User.objects.filter(ref_code = code).count() == 0: break

    return code
class CreateUser(View):

    def post(self, request):
        data = {
            'status':'error',
            'msg':'auth faild'
        }

        if auth_check(authentication.get_authorization_header(request).split()) == False: 
            return JsonResponse(data)

        data.update({"msg":"Can't create user"})
        json_body = json.loads(request.body)
        head = json_body.get('head')
        get_bot_name = json_body.get('bot_name')
        get_usr_id = json_body.get('usr_id')

        if head == 'set_tags':
            data.update({"msg":"can't set tags"})
            get_user = User.objects.get(tg_ID = get_usr_id)
            get_tags_list = json_body.get('tags')

            if json_body.get('tags_action') == 'add':
                for tag_name in get_tags_list:
                    tag = UserTag.objects.get(tag_id = tag_name)
                    try: get_user.tags.add(tag)
                    except: pass
                data.update({"msg":"Tags added"})

            if json_body.get('tags_action') == 'remove':
                for tag_name in get_tags_list:
                    tag = UserTag.objects.get(tag_id = tag_name)
                    try: get_user.tags.remove(tag)
                    except: pass
                data.update({"msg":"Tags removed"})

        if head == 'set_var':
            data.update({"msg":"can't add var"})
            get_var_name = json_body.get('var_name')
            get_var_value = json_body.get('var_value')
            get_user = User.objects.get(tg_ID = get_usr_id)

            try:
                set_var = Var.objects.filter(user = get_user).get(key = get_var_name)
                set_var.value = get_var_value

            except:
                try:
                    set_var = Var(
                        user = get_user,
                        key = get_var_name,
                        value = get_var_value
                    )
                except: pass

            set_var.save()
            data.update({
                'status':'OK',
                'msg':'added new var',
            })

        if head == 'new_user_start':
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
            user.from_bot = tgbot

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

            data.update({
                'status':'OK',
                'msg':'Added new start',
                'prefix':pref,
                'ref':'None'
            })

        return JsonResponse(data)

    def get(self, request):
        data = {
            'status':'error',
            'msg':'auth faild'
        }

        if auth_check(authentication.get_authorization_header(request).split()) == False: 
            return JsonResponse(data)

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

                vars_info = {}
                try: 
                    usr = User.objects.get(tg_ID = user_id)
                    usr_vars = Var.objects.filter(user = usr)

                    for var in usr_vars:
                        vars_info.update({var.key:var.value})
                        
                except: pass
                
                data.update({
                    'status':'OK',
                    'msg':'Done',
                    'vars':vars_info
                })

        return JsonResponse(data)