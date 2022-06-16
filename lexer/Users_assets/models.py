from datetime import date
from django.db import models
from core.models import TgBot

class UserTag(models.Model):
    tag_id = models.CharField(verbose_name = 'Tag ID', max_length = 15, unique = True)
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', null = True, on_delete = models.SET_NULL)
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    priority = models.IntegerField(verbose_name = 'Приоритет', default = 1)
    description = models.TextField(verbose_name = 'Описание тега')
    
    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'
    
    def __str__(self):
        return self.caption

class User(models.Model):
    user_ID = models.CharField(verbose_name = 'ID', max_length = 15, unique = True)
    tg_ID = models.CharField(verbose_name = 'Телеграм ID', max_length = 15)
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', null = True, on_delete = models.SET_NULL)
    name = models.CharField(verbose_name = 'Имя', max_length = 50, default = '', null = True, blank = True)
    tg_nickname = models.CharField(verbose_name = 'Nickname в телеграм', max_length = 50)
    email = models.CharField(verbose_name = 'Адрес электронной почты', max_length = 50, default = '', null = True, blank = True)
    registration_date = models.DateField(verbose_name = 'Дата касания', default = date.today)
    parent_ref_code = models.CharField(verbose_name = 'Родительский рефкод', max_length = 50, default = '', editable = False)
    ping_stat = models.BooleanField(verbose_name = 'Доступность', default = True)
    ref_code = models.CharField(verbose_name = 'Реферальный код', max_length = 10, default = 'markschool', editable = False, unique = True)
    tags = models.ManyToManyField(UserTag, verbose_name = 'Теги', blank = True)
    
    
    def set_active(self):
        self.ping_stat = True
        self.save()
    
    class Meta:
        verbose_name_plural = 'Собеседники'
        verbose_name = 'Собеседник'

    def __str__(self):
        return f'{self.name} ({self.tg_ID}/{self.tg_nickname})' # self.name + ' (' + self.tg_nickname + ')'

class RefLink(models.Model):
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    date = models.DateTimeField(verbose_name = 'Время активации', auto_now = False, auto_now_add = False)
    parent = models.ForeignKey(User, verbose_name = 'Пригласил', on_delete = models.CASCADE, related_name = 'parent')
    child = models.ForeignKey(User, verbose_name = 'Активировал', on_delete = models.CASCADE, related_name = 'child')
    
    def __str__(self):
        return self.caption
    
    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'

class Var(models.Model):
    user = models.ForeignKey(User, verbose_name = 'Собеседник', on_delete = models.CASCADE)
    key = models.CharField(verbose_name = 'Переменная (латиницей)', max_length = 50)
    value = models.CharField(verbose_name = 'Значение', max_length = 150)
    
    def __str__(self):
        return self.key
    
    class Meta:
        verbose_name = 'Переменная'
        verbose_name_plural = 'Переменные'