from django.db import models
from datetime import date
from bot_content.models import keyboard, keyboard_button
import random, string

def get_ref_code():
    while True:
        code = ''.join(random.choices(string.ascii_lowercase, k = 9))
        if Partner.objects.filter(ref_code = code).count() == 0:
            break
    return code

class Bot_config(models.Model):
    bot_name = models.CharField(max_length = 50, verbose_name = 'Имя бота')
    token = models.CharField(max_length = 100, verbose_name = 'API token')
    webhook_host = models.CharField(max_length = 50, verbose_name = 'webhook host', default = 'insiderlab.ru/')
    webhook_port = models.IntegerField(default = 443)
    webhook_url_path = models.CharField(max_length = 100, verbose_name = 'URL path', default = 'bothook/')
    ssl_cert = models.CharField(max_length = 100, verbose_name = 'Path to the ssl certificate', default = '/etc/letsencrypt/live/insiderlab.ru/fullchain.pem')
    ssl_private = models.CharField(max_length = 100, verbose_name = 'Path to the ssl private key', default = '/etc/letsencrypt/live/insiderlab.ru/privkey.pem')
    webapp_host = models.CharField(max_length = 50, verbose_name = 'LAN address to listen webhooks', default = 'localhost')
    webapp_port = models.IntegerField(default = 3001)
    bot_url = models.CharField(verbose_name = 'Bot link', max_length = 50, default = '')
    
    class Meta:
        verbose_name_plural = 'Телеграм боты'
        verbose_name = 'Бот'
    
    def __str__(self):
        return self.bot_name
    
class usr_profile_data(models.Model):
    
    def make_options(keyboard_name):
        options = []
        req_keyboard = keyboard.objects.get(name = keyboard_name)
        for btn in req_keyboard.buttons.all():
            opt = (btn.caption, btn.text)
            options.append(opt)
        return options

    cli_name = models.CharField(verbose_name = 'Имя пользователя', max_length = 50)
    age_cat_b = models.ForeignKey(keyboard_button, related_name = 'age', verbose_name = 'Возростная категория', on_delete = models.CASCADE, limit_choices_to = {'keyboard__name':'age_category_choise_kb'}, null = True, blank = True)
    city = models.CharField(verbose_name = 'Город', max_length = 50)
    invest_value_b = models.ForeignKey(keyboard_button, related_name = 'invest', verbose_name = 'Инвестиционный капитал', on_delete = models.CASCADE, limit_choices_to = {'keyboard__name':'invest_value_kb'}, null = True, blank = True)
    business_expirience_b = models.ForeignKey(keyboard_button, related_name = 'business', verbose_name = 'Опыт предпринимательства', on_delete = models.CASCADE, limit_choices_to = {'keyboard__name':'business_expirience_kb'}, null = True, blank = True)

    class Meta:
        verbose_name_plural = 'Дополнительная информация о пользователях'
        verbose_name = 'Данные'
    
    def __str__(self):
        return self.cli_name

class User(models.Model):
    tg_ID = models.CharField(max_length = 15)
    name = models.CharField(max_length = 50)
    tg_nickname = models.CharField(max_length = 50)
    caption = models.CharField(max_length = 150)
    email = models.CharField(max_length=50, default = '', null = True, blank = True)
    registration_date = models.DateField(default = date.today)
    parent_ref_code = models.CharField(max_length = 50, default = '')
    ping_stat = models.BooleanField(default = True)
    additional_info = models.ForeignKey(usr_profile_data, verbose_name = 'Дополнительная информация', on_delete = models.CASCADE, blank = True, null = True, default = None)
    
    def set_active(self):
        self.ping_stat = True
        self.save()
    
    class Meta:
        verbose_name_plural = 'Люди'
        verbose_name = 'Человек'

    def __str__(self):
        return self.caption
    
class Partner(models.Model):
    ext_name = models.CharField(verbose_name = 'ФИО полностью', max_length = 150)
    rsi_id = models.CharField(verbose_name = 'RSI ID', max_length = 50)
    phone = models.CharField(verbose_name = 'Номер телефона', max_length = 50)
    tg_user = models.ForeignKey(User, verbose_name = "Подписчик телеграм", on_delete = models.CASCADE)
    club_status = models.CharField(verbose_name = 'Клубный статус', max_length = 50)
    exp_date = models.DateField(verbose_name = 'Дата окончания подписки', auto_now = False, auto_now_add = False)
    active = models.BooleanField(verbose_name = 'Активен', default = True)
    ref_code = models.CharField(verbose_name = 'Реферальный код', max_length = 10, default = 'markschool', editable = False, unique = True)
    
    class Meta:
        verbose_name_plural = 'Партнёры'
        verbose_name = 'Партнёр'

    def set_active(self):
        self.active = True
        self.save()
    
    def __str__(self):
        return self.ext_name + ' (' + self.rsi_id + ')' + ' / @' + self.tg_user.tg_nickname

class UserGroup(models.Model):
    G_TYPES = [
        ('local','Локальная группа'),
        ('global','Глобальная группа'),
    ]
    
    name = models.CharField(verbose_name = 'Название переменной для группы (латиницей)', max_length = 50, default = 'new_group')
    caption = models.CharField(verbose_name = 'Отображаемое наименование группы', max_length = 50, default = 'Новая группа')
    g_type = models.CharField(verbose_name = 'Тип группы', max_length = 10, choices = G_TYPES, default = 'global')
    buttons = models.ManyToManyField(keyboard_button, verbose_name = 'По каким кнопкам добавлять в группу', related_name = 'group_additing', blank = True)
    users = models.ManyToManyField(User, verbose_name = 'Члены группы', blank = True)
    
    class Meta:
        verbose_name_plural = 'Группы людей'
        verbose_name = 'Группа людей'
    
    def __str__(self):
        return self.caption

class RefLink(models.Model):
    link_caption = models.CharField(max_length = 128)
    parent = models.ForeignKey(Partner, related_name = 'parent', on_delete = models.CASCADE)
    child = models.OneToOneField(User, related_name = 'child', on_delete = models.CASCADE)
    
    class Meta:
        unique_together = (('parent', 'child'),)
        verbose_name_plural = 'Связи'
        verbose_name = 'Реферальная связь'
    
    def __str__(self):
        return self.link_caption