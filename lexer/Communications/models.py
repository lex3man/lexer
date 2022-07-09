from django.db import models
from Users_assets.models import User
from core.models import TgBot
from django.contrib import admin
from datetime import datetime
import requests

class Sending(models.Model):
    sending_id = models.CharField(verbose_name = 'ID рассылки', max_length = 50)
    creator = models.ForeignKey(User, verbose_name = 'Создатель рассылки', on_delete = models.DO_NOTHING)
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', related_query_name = 'bot', null = True, on_delete = models.SET_NULL)
    create_time = models.DateTimeField(verbose_name = 'Рассылка создана', auto_now = False, auto_now_add = True)
    sending_time = models.DateTimeField(verbose_name = 'Время рассылки', auto_now = False, auto_now_add = False)
    sending_text = models.TextField(verbose_name = 'Текст рассылки')
    in_order = models.BooleanField(verbose_name = 'В очереди', default = False)
    send_done = models.BooleanField(verbose_name = 'Рассылка исполнена', default = False)
    report = models.TextField(verbose_name = 'Отчёт по произведённой рассылке', default = '', blank = True, null = True)
    
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
    
    @admin.action(description = 'Активировать рассылку')
    def shedule(self, queryset):
        for each in queryset:
            if each.sending_time <= datetime.now():
                pass
            else: 
                pass
        queryset.update(in_order = True)
    
    def sending_done(self):
        self.update(send_done = True)
    
    def __str__(self):
        return self.sending_id

class MessageHistory(models.Model):
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', related_query_name = 'bot', null = True, on_delete = models.SET_NULL)
    user = models.ForeignKey(User, verbose_name = 'Создатель рассылки', on_delete = models.DO_NOTHING)
    message_time = models.DateTimeField(verbose_name = 'Время сообщения', auto_now = False, auto_now_add = True)
    message_text = models.TextField(verbose_name = 'Текст сообщения')
    reply = models.TextField(verbose_name = 'Ответ бота', blank = True, null = True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'История сообщений'

    def __str__(self):
        return self.msg_text