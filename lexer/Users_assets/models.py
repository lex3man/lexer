from datetime import date
from django.db import models
from core.models import TgBot

class UserTag(models.Model):
    tag_id = models.CharField(verbose_name = 'Tag ID', max_length = 15, unique = True)
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    priority = models.IntegerField(verbose_name = 'Приоритет', default = 1)
    description = models.TextField(verbose_name = 'Описание тега')
    
    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'
    
    def __str__(self):
        return self.caption

class User(models.Model):
    tg_ID = models.CharField(verbose_name = 'Телеграм ID', max_length = 15, unique = True)
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', null = True, on_delete = models.SET_NULL)
    name = models.CharField(verbose_name = 'Имя', max_length = 50, default = '', null = True, blank = True)
    tg_nickname = models.CharField(verbose_name = 'Nickname в телеграм', max_length = 50)
    email = models.CharField(verbose_name = 'Адрес электронной почты', max_length = 50, default = '', null = True, blank = True)
    registration_date = models.DateField(verbose_name = 'Дата касания', default = date.today)
    parent_ref_code = models.CharField(verbose_name = 'Родительский рефкод', max_length = 50, default = '', editable = False)
    ping_stat = models.BooleanField(verbose_name = 'Доступность', default = True)
    ref_code = models.CharField(verbose_name = 'Реферальный код', max_length = 10, default = 'markschool', editable = False, unique = True)
    tags = models.ManyToManyField(UserTag, verbose_name = 'Теги')
    
    
    def set_active(self):
        self.ping_stat = True
        self.save()
    
    class Meta:
        verbose_name_plural = 'Собеседники'
        verbose_name = 'Собеседник'

    def __str__(self):
        return self.name + ' (' + self.tg_nickname + ')'