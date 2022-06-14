from django.db import models
from bot_content.models import keyboard, keyboard_button, state
from webhook.models import User, Bot_config

class typical_block(models.Model):
    LANG_CHOICES = [
        ('RUS', 'Русский'),
        ('ENG', 'English'),
        ('TUR', 'Turkish'),
        ('GER', 'German'),
        ('FR', 'Frankish'),
    ]
    ENABLE_LIST = [
        ('all','Для всех'),
        ('client','Только для клиентов'),
        ('expartner','Только для неактивных партнеров'),
        ('active','Только для активных партнеров'),
        ('admin','Только для админов'),
    ]

    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    caption = models.CharField(verbose_name = 'Назавание блока', max_length = 50)
    block_id = models.CharField(verbose_name = 'ID блока', max_length = 50, unique = True)
    enable_for = models.CharField(verbose_name = 'Контент для', max_length = 10, choices = ENABLE_LIST, default = 'all')
    text = models.TextField(verbose_name = 'Содержание сообщения')
    state = models.ForeignKey(state, verbose_name = 'Штатная позиция', on_delete = models.CASCADE)
    kb = models.ForeignKey(keyboard, verbose_name = 'Клавиатура', on_delete = models.CASCADE, blank = True, null = True)
    from_button = models.OneToOneField(keyboard_button, verbose_name = 'По какой кнопке появиться', on_delete = models.CASCADE, blank = True, null = True)
    input_data = models.BooleanField(verbose_name = 'Фиксировать введённые данные?', default = False)
    next_block = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True)
    delay_before = models.IntegerField(verbose_name = 'Задержка перед отправкой', default = 0)
    
    class Meta:
        verbose_name = 'Типовой блок сообщения'
        verbose_name_plural = 'Типовые блоки'
    
    def __str__(self):
        return self.caption + ' (' + self.language + ')'
    
class message_history(models.Model):
    date_time = models.DateTimeField(verbose_name = '', auto_now = False, auto_now_add = True)
    bot = models.ForeignKey(Bot_config, verbose_name = '', on_delete = models.DO_NOTHING)
    user = models.ForeignKey(User, verbose_name = '', on_delete = models.PROTECT)
    msg_text = models.TextField(verbose_name = '')
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'История сообщений'

    def __str__(self):
        return self.msg_text

class text_command(models.Model):
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    text = models.CharField(verbose_name = 'Текст команды', max_length = 50)
    go_to = models.ForeignKey(typical_block, verbose_name = 'Вызываемый блок', on_delete = models.CASCADE)
    
    class Meta:
        verbose_name = 'Текстовая команда'
        verbose_name_plural = 'Текстовые команды'
    
    def __str__(self):
        return self.caption + ' (' + self.text + ')'

class client_way(models.Model):
    LANG_CHOICES = [
        ('RUS', 'Русский'),
        ('ENG', 'English'),
        ('TUR', 'Turkish'),
        ('GER', 'German'),
        ('FR', 'Frankish'),
    ]
    
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    caption = models.CharField(verbose_name = 'Назавание блока', max_length = 50)
    block_id = models.CharField(verbose_name = 'ID блока', max_length = 50, unique = True)
    text = models.TextField(verbose_name = 'Содержание сообщения')
    state = models.OneToOneField(state, verbose_name = 'Штатная позиция', on_delete = models.CASCADE)
    kb = models.ForeignKey(keyboard, verbose_name = 'Клавиатура', on_delete = models.CASCADE, blank = True, null = True)
    from_button = models.OneToOneField(keyboard_button, verbose_name = 'По какой кнопке появиться', on_delete = models.CASCADE, blank = True, null = True)
    input_data = models.BooleanField(verbose_name = 'Отправить собранные собранные данные', default = False)
    next_block = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True)
    delay_before = models.IntegerField(verbose_name = 'Задержка перед отправкой', default = 0)

    class Meta:
        verbose_name = 'Сообщение из автоворонки'
        verbose_name_plural = 'Автоворонки'
    
    def __str__(self):
        return self.caption + ' (' + self.language + ')'

class sendings(models.Model):
    
    sending_id = models.CharField(verbose_name = 'ID', max_length = 50, unique = True)
    creator = models.ForeignKey(User, verbose_name = 'Создатель рассылки', on_delete = models.PROTECT)
    create_time = models.DateTimeField(verbose_name = 'Рассылка создана', auto_now = False, auto_now_add = True)
    sending_list = models.CharField(verbose_name = 'Списки для рассылок', max_length = 250)
    sending_time = models.DateTimeField(verbose_name = 'Время рассылки', auto_now = False, auto_now_add = False)
    sending_text = models.TextField(verbose_name = 'Текст рассылки')
    send_done = models.BooleanField(verbose_name = 'Рассылка исполнена', default = False)
    report = models.TextField(verbose_name = 'Отчёт по произведённой рассылке', default = '')
    
    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
    
    def sending_done(self):
        self.send_done = True
        self.save()
    
    def __str__(self):
        return self.sending_id