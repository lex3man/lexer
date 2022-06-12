from django.db import models

class start_content(models.Model):
    LANG_CHOICES = [
        ('RUS', 'Русский'),
        ('ENG', 'English'),
        ('TUR', 'Turkish'),
        ('GER', 'German'),
        ('FR', 'Frankish'),
    ]
    
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    
    hello_message = models.TextField(verbose_name = 'Приветственное сообщение', default = '')
    get_user_name = models.TextField(verbose_name = 'Предложение познакомиться и запрос имени', default = '')
    data_access_error = models.TextField(verbose_name = 'Текст при ошибке доступа к базе пользователей', default = '')
    name_verify_welcome = models.TextField(verbose_name = 'Проверка имени при повторном использовании команды "start" зарегистрированного пользователя', default = '')
    wrong_chat_message = models.TextField(verbose_name = 'Сообщение, если команда "start" написана в общем чате', default = '')
    welcome_message_with_name = models.TextField(verbose_name = 'Сообщение от бота, после того, как пользователь представился', default = '')
    user_reg_error_message = models.TextField(verbose_name = 'Сообщение при ошибке захвата имени пользователя', default = '')
    new_name_please = models.TextField(verbose_name = 'Проедложение ввести новое имя, если сохранено неверное', default = '')
    right_name = models.TextField(verbose_name = 'Сообщение после того, как пользователь подтвердил своё имя', default = '')
    
    class Meta:
        verbose_name = 'Содержание первых сообщений от бота'
        verbose_name_plural = 'Содержание первых сообщений от бота'
    
    def __str__(self):
        return self.language

class keyboard_button(models.Model):
    ALLOW_GROUP = [
        ('all','Для всех'),
        ('client','Только для клиентов'),
        ('expartner','Только для неактивных партнеров'),
        ('active','Только для активных партнеров'),
        ('admin','Только для админов'),
        ('other','Для другой группы'),
    ]
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    text = models.CharField(verbose_name = 'Текст кнопки', max_length = 50)
    order = models.IntegerField(verbose_name = 'Номер строки размещения кнопки', default = 1)
    visibls_for = models.CharField(verbose_name = 'Для каких пользователей доступна кнопка', max_length = 10, choices = ALLOW_GROUP, default = 'all')
    #another = models.ForeignKey(UserGroup, verbose_name = 'Гругая группа пользователей', on_delete = models.CASCADE, blank = True, default = 1)
    
    class Meta:
        verbose_name = 'Кнопка клавиатуры'
        verbose_name_plural = 'Кнопки для клавиатур'
    
    def __str__(self):
        return self.text

class keyboard(models.Model):
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    name = models.CharField(verbose_name = 'Имя переменной клавиатуры', max_length = 50)
    LANG_CHOICES = [
        ('RUS', 'Русский'),
        ('ENG', 'English'),
        ('TUR', 'Turkish'),
        ('GER', 'German'),
        ('FR', 'Frankish'),
    ]
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    buttons = models.ManyToManyField(keyboard_button, verbose_name = 'Кнопки', related_query_name = 'keyboard')
    
    class Meta:
        verbose_name = 'Клавиатура'
        verbose_name_plural = 'Клавиатуры'
    
    def __str__(self):
        return self.language + ' / ' + self.caption

class social_link(models.Model):
    SOCIALS = [
        ('YT','YouTube'),
        ('VK','Vkontakte'),
        ('IG','Instagram'),
        ('FB','Facebook'),
        ('TG','Telegram'),
        ('DC','Discord'),
        ('TK','TikTok'),
        ('VB','Viber'),
        ('ST','Site')
    ]
    link_name = models.CharField(verbose_name = 'Назнание для ссылки (отображаться не будет)', max_length = 50)
    social = models.CharField(verbose_name = 'Площадка', max_length = 5, choices = SOCIALS)
    link_url = models.CharField(verbose_name = 'Ссылка на канал/профиль', max_length = 250)
    
    class Meta:
        verbose_name = 'Ссылка на соцсеть'
        verbose_name_plural = 'Ссылки на соцсети'
    
    def __str__(self):
        return self.link_name
    
class links_group(models.Model):
    PERMITION_CLASS = [
        (0, 'Open for all'),
        (1, 'Partners ever'),
        (2, 'Active status only'),
        (3, 'Top only'),
        (4, 'Admins only'),
    ]
    group_name = models.CharField(verbose_name = 'Наименование группы ссылок', max_length = 50)
    permition_class = models.IntegerField(verbose_name = 'Уровень доступа', default = 0, choices = PERMITION_CLASS)
    links = models.ManyToManyField(social_link, verbose_name = 'Ссылки (можно выбрать несколько)')
    
    class Meta:
        verbose_name = 'Группа ссылок'
        verbose_name_plural = 'Группы ссылок'
    
    def __str__(self):
        return self.group_name
    
class main_menu_reaction(models.Model):
    LANG_CHOICES = [
        ('RUS', 'Русский'),
        ('ENG', 'English'),
        ('TUR', 'Turkish'),
        ('GER', 'German'),
        ('FR', 'Frankish'),
    ]
    
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    
    follow_us = models.TextField(verbose_name = 'Сообщение перед ссылками на соцсети', default = '')
    rsi_detail = models.TextField(verbose_name = 'Подробнее о RSI', default = '')
    more = models.TextField(verbose_name = 'Варианты заработка с RSI (продукты)', default = '')
    lk = models.TextField(verbose_name = 'Личный кабинет', default = '')
    
    class Meta:
        verbose_name = 'Ответ на кнопки главного меню'
        verbose_name_plural = 'Ответ на кнопки главного меню'
    
    def __str__(self):
        return self.language

class state(models.Model):
    name = models.CharField(verbose_name = 'Имя переменной', max_length = 50, default = 'name_state')
    caption = models.CharField(verbose_name = 'Отображаемое название позиции', max_length = 50, default = 'Новая позиция')
    state_id = models.CharField(verbose_name = 'ID позиции', max_length = 50, unique = True)
    
    class Meta:
        verbose_name = 'Состояние бота'
        verbose_name_plural = 'Состояния бота для пользователя'
    
    def __str__(self):
        return self.caption