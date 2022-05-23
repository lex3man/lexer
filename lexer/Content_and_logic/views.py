from difflib import Match
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import keyboard, keyboard_button, Command
from core.models import TgBot
from core.views import auth_check

from rest_framework import authentication

import json

class Get_content(View):
    def get(self, request):
        data = {'status':'error'}
        auth_header = auth_check(authentication.get_authorization_header(request).split())
        if auth_header == False: return JsonResponse(data)
        
        json_body = json.loads(request.body)
        exec_bot = TgBot.objects.get(token = json_body['bot_token'])
        header = json_body['head']
        try:
            cont = {}
            
            match header:
                case 'buttons': 
                    items = keyboard_button.objects.filter(from_bot = exec_bot)
                    fields_info = keyboard_button._meta.get_fields()
                case 'commands': 
                    items = Command.objects.filter(from_bot = exec_bot)
                    fields_info = Command._meta.get_fields()
            
            data.update({'status':'OK'})
            for get_item in items:
                get_fields_info = {}
                for field_info in fields_info:
                    try:
                        ser_data = str(json.dumps(getattr(get_item, field_info.name), separators=(',', ':'), ensure_ascii = False, default = str)).replace('"','')
                    except: ser_data = ''
                    get_fields_info.update({field_info.name:ser_data})
                cont.update({get_item.caption:get_fields_info})
            data.update({header:cont})
                
        except: pass
        return JsonResponse(data)