from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.views import View

from rest_framework import authentication
from bearer_auth.models import AccessToken

from .models import TgBot, EnvVar

def Index(request):
    template = loader.get_template('index.html')
    cont = {}
    return HttpResponse(template.render(cont, request))

# Проверка токена
def auth_check(auth_header):
    if not auth_header:
        return False
    if len(auth_header) == 1:
        return False
    elif len(auth_header) > 2:
        return False
    try:
        token = auth_header[1].decode('utf-8')
        AccessToken.objects.get(key = token)
        return True
    except: return False

# Отображение переменных окружения
class Env_vars(View):
    def get(self, request):
        data = {}
        for var in EnvVar.objects.all():
            data.update({
                    var.caption:{
                        'description':var.description,
                        'value':var.value
                    }
            })
        return JsonResponse(data)

# Ответ на запрос информации о боте по имени
class Bot_info(View):
    def get(self, request):

        auth_header = auth_check(authentication.get_authorization_header(request).split())
        data = {'status':'error'}

        if auth_header:
            bot_name = request.GET.get('bot_name')
            bots = TgBot.objects.filter(caption = bot_name)
            if bot_name == 'all': bots = TgBot.objects.all()

            for bot in bots:
                data.update({
                    'status':'success',
                    bot.caption:{
                        'token':bot.token,
                        'description':bot.description,
                        'url':bot.url,
                        'active':bot.active
                    }
                })
            return JsonResponse(data)
        else:
            return JsonResponse(data)