from django.db import models
import requests
from django.contrib import admin
from django.utils.html import format_html

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
    active = models.BooleanField(verbose_name = 'Активен', default = False, editable = True)

    def __str__(self):
        return self.caption

    @admin.action(description = 'Запустить выбранных ботов')
    def start(self, request, queryset):
        queryset.update(active = True)
        for b in queryset:
            try: requests.post('http://127.0.0.1:5000', json = {'bot_name':b.caption, 'action':'add'})
            except: 
                b.active = False
                b.save()

    @admin.action(description = 'Остановить выбранных ботов')
    def stop(self, request, queryset):
        queryset.update(active = False)
        for b in queryset:
            try: requests.post('http://127.0.0.1:5000', json = {'bot_name':b.caption, 'action':'remove'})
            except: pass

    @admin.display
    def add_action(self):
        if self.active: return format_html('<button class="stop_btn">Остановить</button>')
        return format_html('<button class="start_btn">Запустить</button>')

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Телеграм боты'