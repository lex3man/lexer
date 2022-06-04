from django.db import models
import requests

class EnvVar(models.Model):
    caption = models.CharField(verbose_name = 'Имя переменной (только латиница)', max_length = 50, unique = True)
    description = models.CharField(verbose_name = 'Описание переменной', max_length = 150, blank = True, null = True)
    value = models.CharField(verbose_name = 'Значение переменной', max_length = 200)
    
    def __str__(self):
        return self.caption
    
    class Meta:
        verbose_name = 'Переменная окружения'
        verbose_name_plural = 'Переменные окружения'

class TgBot(models.Model):
    caption = models.CharField(verbose_name = 'Наименование бота', max_length = 50, unique = True)
    description = models.CharField(verbose_name = 'Описание', max_length = 150, blank = True, null = True)
    url = models.CharField(verbose_name = 'Ссылка на бота', max_length = 150)
    token = models.CharField(verbose_name = 'API token телеграм бота', max_length = 150)
    active = models.BooleanField(verbose_name = 'Активен', default = True, editable = True)
    
    def __str__(self):
        return self.caption
    
    def start(self):
        self.active = True
        resp = requests.post('http://127.0.0.1:5000', json = {'bot_name':self.caption, 'action':'add'})
        return resp
        
    def stop(self):
        self.active = False
        resp = requests.post('http://127.0.0.1:5000', json = {'bot_name':self.caption, 'action':'remove'})
        return resp
    
    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Телеграм боты'