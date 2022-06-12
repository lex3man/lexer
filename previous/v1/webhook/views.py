from django.http import HttpResponse, request, JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from datetime import date, datetime
from bot_content.models import keyboard, keyboard_button

import json, requests

from .models import Bot_config, User, RefLink, Partner, get_ref_code, usr_profile_data, UserGroup

def get_kb_buttons_data(req_keyboards_names):
    buttons_data = {}
    for kb in req_keyboards_names:
        req_keyboard = keyboard.objects.get(name = kb)
        btns = {}
        for btn in req_keyboard.buttons.all():
            btns.update({btn.text:btn.caption})
        buttons_data.update({req_keyboard.name:btns})
    return buttons_data

def home(View):
    return HttpResponse('Сайт пока находится в разработке!<br>\
        <a href="https://lexer.insiderlab.ru/admin">ADMINka</a><br><br>')

def RSI_webhook(data):
    auth_token = '$zZ*ikCvz8DT5QI7T7*yBv0kbnFsz*Bz6oD09nb86zWTrlZbHRtvvPqRk@*i%%zI'
    head = {'Authorization': 'Bearer ' + auth_token}
    req = {
        'club_status':'/club',
        'carier_stat':'/binary/info',
        'cusator':'/user/curator',
        'ref_link':'/ref',
        'usr_info':'/user/view'
    }
    req_url = 'https://api.rsi.wocom.biz/tg1'
    resp_api = requests.get(req_url + req[data['pref']], params = {'id':data['id']}, headers = head)
    return resp_api.json()

class API_hook_config(View):
    def post(self, request):
        json_body = json.loads(request.body)
        get_bot_name = json_body.get('bot_name')
        bot_conf = Bot_config.objects.get(bot_name = get_bot_name)
        data = {
            'TOKEN':bot_conf.token,
            'WEBHOOK_HOST':bot_conf.webhook_host,
            'WEBHOOK_PORT':bot_conf.webhook_port,
            'WEBHOOK_URL_PATH':bot_conf.webhook_url_path,
            'WEBHOOK_SSL_CERT':bot_conf.ssl_cert,
            'WEBHOOK_SSL_PRIV':bot_conf.ssl_private,
            'WEBAPP_HOST':bot_conf.webapp_host,
            'WEBAPP_PORT':bot_conf.webapp_port
        }
        return JsonResponse(data)

class get_data(View):
    def post(self, request):
        json_body = json.loads(request.body)
        head = json_body.get('head')
        data = {}
        get_usr_id = json_body.get('usr_id')
        try:
            user = User.objects.get(tg_ID = str(get_usr_id))
            
            # Первичный ассесмент клиента
            if head == 'assessment_finish_state':
                data.update({
                    'cli_name':json_body.get('client_way_start_state'),
                    'age_cat':json_body.get('age_state'),
                    'city':json_body.get('City_state'),
                    'invest_value':json_body.get('invest_value_state'),
                    'business_expirience':json_body.get('business_expirience_state')
                })
                keybs = ['age_category_choise_kb', 'invest_value_kb', 'business_expirience_kb']
                buttons_data = get_kb_buttons_data(keybs)
                assessment = usr_profile_data(
                    cli_name = data['cli_name'],
                    age_cat_b = keyboard_button.objects.get(caption = buttons_data[keybs[0]][data['age_cat']]),
                    city = data['city'],
                    invest_value_b = keyboard_button.objects.get(caption = buttons_data[keybs[1]][data['invest_value']]),
                    business_expirience_b = keyboard_button.objects.get(caption = buttons_data[keybs[2]][data['business_expirience']])
                )
                assessment.save()
                user.additional_info = assessment
                user.save()
                
                # добавить в группу пользователей
                try:
                    add_to_groups = UserGroup.objects.filter(name = 'with_data')
                    add_to_groups = add_to_groups.union(UserGroup.objects.filter(buttons = assessment.invest_value_b))
                    add_to_groups = add_to_groups.union(UserGroup.objects.filter(buttons = assessment.business_expirience_b))
                    for g in add_to_groups:
                        g.users.add(user)
                except:
                    group = UserGroup.objects.get(name = 'with_data')
                    group.users.add(user)
                
                data.update({'status':'OK', 'msg':str(data)})

            # Запрос информации о партнёре
            if head == 'part_info':
                partner = Partner.objects.get(tg_user = user)
                attr_count = 0
                attrs = []
                for field in Partner._meta.get_fields():
                    attr_count += 1
                    attrs.append(field.name)
                data.update(model_to_dict(partner))
                data.update({'ref_code':partner.ref_code})
                data.update({'attrs':attrs, 'status':'OK'})

            # Редактирование информации о пользователе
            if head == 'update_name':
                user.name = json_body.get('name')
                user.save()
                data.update({'status':'OK'})

            # Запрос информации о группах пользователей
            if head == 'groups_info':
                ginfo = {}
                for grp in UserGroup.objects.all():
                    content = {
                        'name':grp.caption,
                        'members':grp.users.count(),
                    }
                    ginfo.update({grp.name:content})
                data.update({'status':'OK', 'groups':ginfo})
            
            # Запрос состава группы
            if head == 'group_members':
                group_name = json_body.get('group')
                if group_name == 'all': grps = UserGroup.objects.all()
                else: grps = UserGroup.objects.filter(name = group_name)
                usrs_in_group = {}
                for grp in grps:
                    for u in grp.users.all():
                        usrs_in_group.update({
                            u.tg_ID:{
                                'name':u.name,
                                'tg_id':u.tg_nickname,
                                'available':u.ping_stat
                            }
                        })
                data.update({'status':'OK', 'users':usrs_in_group})
            
            # Запрос информации о пользователе
            if head == 'user_info':
                attr_count = 0
                attrs = []
                for field in User._meta.get_fields():
                    attr_count += 1
                    attrs.append(field.name)
                data.update(model_to_dict(user))
                groups_info = []
                try:
                    groups = UserGroup.objects.filter(users = user)
                    for grp in groups:
                        groups_info.append(grp.name)
                except: groups_info.append('NONE')
                data.update({'attrs':attrs, 'groups':groups_info, 'status':'OK'})

        except: data.update({'status':'error', 'msg':'Такого пользователя не зарегистрированно'})

        return JsonResponse(data)

class add_or_edit_obj(View):
    def post(self, request):
        json_body = json.loads(request.body)
        head = json_body.get('head')
        data = {'status':'error'}

        # Доступные префиксы:
        # 'club_status'
        # 'carier_stat'
        # 'cusator'
        # 'ref_link'
        # 'usr_info'

        # Регистрация новых данных от пользователя
        if head == 'upcoming_data':
            up_data = json_body.get('stack')
            usr_id = up_data['usr_id']
            for k in up_data.keys(): state = k

            # Регистрация действующего партнера
            if state == 'rsi_id_state':
                part_id = int(up_data[state])
                msg = 'Что-то пошло не так...'
                st = 'error'

                # Проверяем подлинность запроса
                resp_api = RSI_webhook({'id':part_id, 'pref':'usr_info'})
                verify = False
                if resp_api['status'] == 200:
                    msg = 'Данные не подтверждены. \nВозможно была допущенна ошибка. Проверьте правильность введённых данных и их соответствие в личном кабинете!'
                    user_data = resp_api['data']
                    if str(up_data['email_state']).lower() == str(user_data['email']).lower():
                        verify = True
                        msg = 'Данные подтверждены'
                    if str(user_data['tg']).replace('@','') == up_data['tg_username']:
                        verify = True
                        msg = 'Данные подтверждены'

                # Создаём новую запись
                resp_api = RSI_webhook({'id':part_id, 'pref':'club_status'})
                if resp_api['status'] == 200 and verify == True:
                    exp_date_time = datetime.now()
                    act_status = False
                    msg = 'Ваш клубный статус истёк или не активен'
                    st = 'error'
                    if resp_api['data'] != None:
                        date_time_str = resp_api['data']['activeTo']
                        dateFormatter = '%d.%m.%Y %H:%M:%S'
                        exp_date_time = datetime.strptime(date_time_str, dateFormatter)
                        act_status = True
                        resp_api = RSI_webhook({'id':part_id, 'pref':'carier_stat'})
                        carier_stat = 'Нет'
                        if resp_api['data']['currentStatus'] != None: carier_stat = resp_api['data']['currentStatus']['name']
                        resp_api = RSI_webhook({'id':part_id, 'pref':'usr_info'})
                        part_info = resp_api['data']
                        try:
                            new_part = Partner(
                                ext_name = part_info['first_name'] + ' ' + part_info['last_name'], 
                                rsi_id = part_id, 
                                phone = part_info['phone'], 
                                tg_user = User.objects.get(tg_ID = usr_id), 
                                club_status = carier_stat,
                                exp_date = exp_date_time, 
                                active = act_status, 
                                ref_code = get_ref_code()
                            )
                            new_part.save()
                            st = 'OK'
                            msg = 'Вы успешно активировали статус партнёра'
                        except:
                            st = 'error'
                            msg = 'Косяк при создании'
                data.update({'status':st,'msg':msg})

        # Добавить нового пользователя
        if head == 'new_user':
            get_usr_id = json_body.get('usr_id')
            get_usr_name = json_body.get('name')
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
                user = User(
                    tg_ID = get_usr_id,
                    name = get_usr_name,
                    tg_nickname = get_usr_tg,
                    caption = get_usr_name + ' (@%s)' % get_usr_tg,
                    registration_date = date.today(),
                    parent_ref_code = get_usr_ref
                )
                user.save()
                if ref_code != 'None':
                    parent = Partner.objects.get(ref_code = ref_code)
                    RefLink.objects.create(parent = parent, child = user, link_caption = parent.ext_name + ' (' + parent.rsi_id + ') / ' + user.name)
                data.update({'status':'OK','pref':pref})
            except:
                data.update({'status':'error', 'msg':'Не получилось зарегистрировать пользователя'})

        return JsonResponse(data)