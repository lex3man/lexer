from pyexpat import model
from django.db import models

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
    caption = models.CharField(verbose_name = 'Наименование бота', max_length = 50)
    description = models.CharField(verbose_name = 'Описание', max_length = 150, blank = True, null = True)
    url = models.CharField(verbose_name = 'Ссылка на бота', max_length = 150)
    token = models.CharField(verbose_name = 'API token телеграм бота', max_length = 150)
    active = models.BooleanField(verbose_name = 'Активен', default = True)
    
    def __str__(self):
        return self.caption
    
    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Телеграм боты'