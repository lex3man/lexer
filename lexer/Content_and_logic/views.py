from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import keyboard, keyboard_button, Command, FirstTouch
from core.models import TgBot
from core.views import auth_check

from rest_framework import authentication

import json

class Get_content(View):
    def get(self, request):
        data = {'status':'error'}
        auth_header = auth_check(authentication.get_authorization_header(request).split())
        if auth_header == False: return JsonResponse(data)
        
        header = request.GET.get('head')
        bot_name = request.GET.get('botname')
        exec_bot = TgBot.objects.get(caption = bot_name)
        
        try:
            cont = {}
            match header:
                case 'buttons': 
                    items = keyboard_button.objects.filter(from_bot = exec_bot)
                    fields_info = keyboard_button._meta.get_fields()
                case 'commands': 
                    items = Command.objects.filter(from_bot = exec_bot)
                    fts = FirstTouch.objects.filter(from_bot = exec_bot)
                    fields_info = Command._meta.get_fields()
                    conditions = {}
                    for item in items:
                        info = {}
                        for item_cond in item.conditions.all():
                            try: 
                                tag = item_cond.usr_tag
                                t_id = tag.tag_id
                            except: t_id = "None"
                            info.update({item_cond.name:{
                                'var_key':item_cond.var_key,
                                'qual':item_cond.qual,
                                'var_value':item_cond.var_value,
                                'usr_tag':t_id,
                                'failed_text':item_cond.failed_text
                            }})
                        conditions.update({item.caption:info})
                    first_touch = {}
                    for ft in fts:
                        try: kb_name = ft.keyboard.name
                        except: kb_name = 'None'
                        info = {
                            'text':ft.text,
                            'keyboard':kb_name,
                            'input_state':ft.input_state,
                            'next_block':ft.next_block
                        }
                        first_touch.update({
                            ft.language:info
                        })
                    data.update({
                        'conditions':conditions,
                        'first_touch':first_touch
                    })
                case 'keyboard':
                    keyboards = keyboard.objects.filter(from_bot = exec_bot)
                    for kb in keyboards:
                        buttons = kb.buttons.all()
                        btns = {}
                        for btn in buttons:
                            btns.update({btn.caption:[btn.text, btn.order]})
                        cont.update({kb.name:btns})
            
            data.update({'status':'OK'})
            try:
                for get_item in items:
                    get_fields_info = {}
                    for field_info in fields_info:
                        try: ser_data = str(json.dumps(getattr(get_item, field_info.name), separators=(',', ':'), ensure_ascii = False, default = str)).replace('"','')
                        except: ser_data = ''
                        get_fields_info.update({field_info.name:ser_data})
                    cont.update({get_item.caption:get_fields_info})
            except: pass
            data.update({header:cont})
                
        except: pass
        return JsonResponse(data)