from django.http import JsonResponse, request, HttpResponse
from django.forms.models import model_to_dict
from django.views import View
from .models import keyboard, start_content, links_group, main_menu_reaction, state, keyboard_button
from bot_logic.models import typical_block, text_command, client_way
from webhook.models import User, Partner, UserGroup

def index(request):
    return HttpResponse("Контент нада?!")

class get_content(View):
    def get(self, request):
        lang = request.GET.get('lang', 'RUS')
        get_state = request.GET.get('state')
        data = {'language':lang}

        # Получаем список штатных позиций блоков
        if get_state == 'get_states':
            all_positions = state.objects.all()
            states_pos = {}
            for position in all_positions:
                states_pos.update({position.name:[position.caption, position.state_id]})
            data.update({'status':'OK','states':states_pos})

        # Контент для команды START
        if get_state == 'start_cont':
            try:
                start_cont = start_content.objects.get(language = lang)
                get_start_content = {}
                for field in start_content._meta.get_fields():
                    get_start_content.update({field.name:field.value_from_object(start_cont)})
                data.update({
                    'status':'OK',
                    'start_cont':get_start_content
                })
            except:
                data.update({'status':'error', 'msg':'Не нашлось контента'})

        # Контент для клавиатуры    
        if get_state == 'kb_buttons':
            kbs = keyboard.objects.filter(language = lang)
            cmds = text_command.objects.all()
            kbs_cont = {}
            vis_for_list = ['all']
            try:
                usr_id = request.GET.get('user_id')
                usr = User.objects.get(tg_ID = usr_id)
                try:
                    admin_group = UserGroup.objects.get(name = 'admin_group')
                    for admin in admin_group.users.all():
                        if usr == admin: is_admin = True
                    if is_admin: 
                        status = 'admin'
                    else: status = 'not admin'
                    vis_for_list.append(status)
                except: pass
                try: 
                    part_status = Partner.objects.get(tg_user = usr)
                    status = 'expartner'
                    if part_status.active == True: status = 'active'
                except:
                    status = 'client'
                vis_for_list.append(status)
            except:
                status = 'super_admin'
            for kb in kbs:
                kb_buttons = {}
                for btn in kb.buttons.all(): 
                    if status == 'super_admin': kb_buttons.update({btn.caption:[btn.text, btn.order]})
                    if btn.visibls_for in vis_for_list: 
                        kb_buttons.update({btn.caption:[btn.text, btn.order]})
                kbs_cont.update({kb.name:kb_buttons})
            commands = {}
            for cmd in cmds:
                get_block = cmd.go_to
                get_kb = get_block.kb
                commands.update({cmd.caption:[cmd.text, get_kb.name]})
            kbs_cont.update({'commands':commands})
            data.update({'status':'OK', get_state:kbs_cont, 'vis_list':vis_for_list, 'sts':status})

        # Контент для получения ссылок на соцсети
        if get_state == 'social_cont':
            usr_id = request.GET.get('user_id')
            user = User.objects.get(tg_ID = usr_id)
            try:
                partner = Partner.objects.get(tg_user = user)
                p_status = 'partner'
                if partner.active == True: p_status = 'active partner'
            except: p_status = 'client'

            if p_status == 'client': 
                get_links_group = links_group.objects.all().filter(permition_class = 0)
            elif p_status == 'partner': 
                try: get_links_group = links_group.objects.all().filter(permition_class = 1)
                except: get_links_group = links_group.objects.all().filter(permition_class = 0)
            elif p_status == 'active partner': 
                try: get_links_group = links_group.objects.all().filter(permition_class = 2)
                except:
                    try: get_links_group = links_group.objects.all().filter(permition_class = 1)
                    except: get_links_group = links_group.objects.all().filter(permition_class = 0)
            groups = {}
            for l_group in get_links_group:
                links = {}
                for link in l_group.links.all():
                    links.update({link.link_name:link.link_url})
                groups.update({l_group.group_name:links})
            text = main_menu_reaction.objects.get(language = lang)
            data.update({'status':'OK', 'social_cont':groups, 'text':text.follow_us})

        # контент для "подробностей об RSI"
        if get_state == 'rsi_details':
            content = {}
            text = main_menu_reaction.objects.get(language = lang)
            data.update({'status':'OK', 'rsi_details':content, 'text':text.rsi_detail})

        # Запрос стандартного блока по block_id
        if get_state == 'block_id':
            blk_id = request.GET.get('additional')
            try:
                use_block = typical_block.objects.get(block_id = blk_id)
                block_state = use_block.state
                block_kb = use_block.kb
                input_mode = 'no'
                next_block_id = ''
                if use_block.input_data == True: 
                    input_mode = 'yes'
                    next_block = use_block.next_block
                    next_block_id = next_block.block_id
                block_content = {
                    'text':use_block.text,
                    'delay':use_block.delay_before,
                    'state':block_state.name,
                    'keyboard':block_kb.name,
                    'input':input_mode,
                    'next':next_block_id
                }
                data.update({'status':'OK','block_cont':block_content})
            except:
                data.update({'status':'error'})

        # Запрос контента для автоворонки
        if get_state == 'client_way_start_state':
            get_user_id = request.GET.get('user_id')
            user = User.objects.get(tg_ID = get_user_id)
            additional_data = request.GET.get('additional').split('__')
            try:
                get_btn_text = additional_data[0]
                get_prev_block_state = additional_data[1]
                try:
                    get_btn = keyboard_button.objects.get(text = get_btn_text)
                    start_block = client_way.objects.get(from_button = get_btn)
                except:
                    prev_block = client_way.objects.get(state__name = get_prev_block_state)
                    start_block = prev_block.next_block
            except:
                block_state = state.objects.get(name = get_state)
                start_block = client_way.objects.get(state = block_state)
            try:
                block_kb = start_block.kb
                kb_name = block_kb.name
            except: kb_name = 'None'
            block_state = start_block.state
            block_content = model_to_dict(start_block)
            block_content.update({'keyboard':kb_name, 'state':block_state.name})
            data.update({'status':'OK','block_cont':block_content})

        # Запрос стандартного блока по кнопке
        if get_state == 'stblck':
            msg = request.GET.get('additional')
            get_user_id = request.GET.get('user_id')
            user = User.objects.get(tg_ID = get_user_id)
            admin_group = UserGroup.objects.get(name = 'admin_group')
            for admin in admin_group.users.all():
                if user == admin: is_admin = True
            try:
                partner = Partner.objects.get(tg_user = user)
                user_stat = 'expartner'
                if partner.active == True:
                    user_stat = 'active'
            except: user_stat = 'client'
            block_content = {
                'text':'Сейчас для вас этот раздел не доступен',
                'delay':0,
                'state':'main_state',
                'keyboard':'empty_kb',
                'input':'no',
                'next':''
            }
            try:
                use_block = typical_block.objects.get(from_button__text = msg)
                if use_block.enable_for == user_stat or use_block.enable_for == 'all' or is_admin:
                    block_state = use_block.state
                    block_kb = use_block.kb
                    input_mode = 'no'
                    next_block_id = ''
                    if use_block.input_data == True: 
                        input_mode = 'yes'
                        next_block = use_block.next_block
                        next_block_id = next_block.block_id
                    block_content = {
                        'text':use_block.text,
                        'delay':use_block.delay_before,
                        'state':block_state.name,
                        'keyboard':block_kb.name,
                        'input':input_mode,
                        'next':next_block_id
                    }
                data.update({'status':'OK','block_cont':block_content})
            except:
                try:
                    goto = text_command.objects.get(text = msg)
                    use_block = goto.go_to
                    if use_block.enable_for == user_stat or use_block.enable_for == 'all' or is_admin:
                        block_state = use_block.state
                        block_kb = use_block.kb
                        input_mode = 'no'
                        next_block_id = ''
                        if use_block.input_data == True:
                            input_mode = 'yes'
                            next_block = use_block.next_block
                            next_block_id = next_block.block_id
                        block_content = {
                            'text':use_block.text,
                            'delay':use_block.delay_before,
                            'state':block_state.name,
                            'keyboard':block_kb.name,
                            'input':input_mode,
                            'next':next_block_id
                        }
                    data.update({'status':'OK','block_cont':block_content})
                except:
                    data.update({'status':'error'})

        return JsonResponse(data)
