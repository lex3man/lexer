from django.db import models
from core.models import TgBot
from Users_assets.models import UserTag

LANG_CHOICES = [
        ('RUS', 'Русский'),
        ('ENG', 'English'),
        ('TUR', 'Turkish'),
        ('GER', 'German'),
        ('FR', 'Frankish'),
    ]

class keyboard_button(models.Model):
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', related_query_name = 'bot', null = True, on_delete = models.SET_NULL)
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50, unique = True)
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    text = models.CharField(verbose_name = 'Текст кнопки', max_length = 50)
    order = models.IntegerField(verbose_name = 'Номер строки размещения кнопки', default = 1)
    
    class Meta:
        verbose_name = 'Кнопка клавиатуры'
        verbose_name_plural = 'Кнопки для клавиатур'
    
    def __str__(self):
        return self.text

class keyboard(models.Model):
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', related_query_name = 'bot', null = True, on_delete = models.SET_NULL)
    caption = models.CharField(verbose_name = 'Наименование', max_length = 50)
    name = models.CharField(verbose_name = 'Имя переменной клавиатуры', max_length = 50, unique = True)
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    buttons = models.ManyToManyField(keyboard_button, verbose_name = 'Кнопки', related_query_name = 'keyboard')
    
    class Meta:
        verbose_name = 'Клавиатура'
        verbose_name_plural = 'Клавиатуры'
    
    def __str__(self):
        return self.name 

class Condition(models.Model):
    QUAL_CHOISE = [
        ('=', 'РАВНО'), 
        ('>=', 'БОЛЬШЕ-РАВНО'), 
        ('>', 'БОЛЬШЕ'), 
        ('<=', 'МЕНЬШЕ-РАВНО'), 
        ('<', 'МЕНЬШЕ')
    ]
    
    name = models.CharField(verbose_name = 'Наименование', max_length = 50)
    var_key = models.CharField(verbose_name = 'Переменная', max_length = 50, blank = True, null = True)
    qual = models.CharField(verbose_name = 'Сравнение', max_length = 2, choices = QUAL_CHOISE, default = '=')
    var_value = models.CharField(verbose_name = 'Значение', max_length = 150, blank = True, null = True)
    usr_tag = models.ForeignKey(UserTag, verbose_name = 'ИЛИ по тегу', on_delete = models.CASCADE, blank = True, null = True)
    failed_text = models.TextField(verbose_name = 'Текст при неудаче', blank = True, null = True)
    
    class Meta:
        verbose_name = 'Условие'
        verbose_name_plural = 'Условия'
    
    def __str__(self):
        return self.name

class TypeBlock(models.Model):
    block_id = models.CharField(verbose_name = 'ID', max_length = 50, unique = True)
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', null = True, on_delete = models.SET_NULL)
    from_button = models.ManyToManyField(keyboard_button, verbose_name = 'По кнопке', blank = True)
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    text = models.TextField(verbose_name = 'Текст реакции', blank = True, null = True)
    keyboard = models.ForeignKey(keyboard, verbose_name = 'Клавиатура', on_delete = models.SET_NULL, blank = True, null = True, default = None)
    input_state = models.BooleanField(verbose_name = 'Ожидание ввода?', default = False)
    save_to_var = models.CharField(verbose_name = 'Имя переменной для сохранения ввода', max_length = 50, blank = True, null = True, default = None)
    value_to_save = models.CharField(verbose_name = 'Значение переменной (если ввод не ожидается)', max_length = 150, blank = True, null = True, default = None)
    next_block = models.ForeignKey('self', verbose_name = 'Следующий блок', null = True, blank = True, on_delete = models.SET_NULL)
    delay = models.IntegerField(verbose_name = 'Задержка перед реакцией (секунды)', default = 0)
    conditions = models.ManyToManyField(Condition, verbose_name = 'Условия', blank = True)

    class Meta:
        verbose_name = 'Типовой блок'
        verbose_name_plural = 'Типовые блоки (сообщения от бота)'
    
    def __str__(self):
        return self.block_id

class Command(models.Model):
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', null = True, on_delete = models.SET_NULL)
    command_id = models.CharField(verbose_name = 'ID', max_length = 10, unique = True)
    caption = models.CharField(verbose_name = 'Команда (латиницей)', max_length = 50)
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    text = models.TextField(verbose_name = 'Текст реакции', blank = True, null = True)
    keyboard = models.ForeignKey(keyboard, verbose_name = 'Клавиатура', on_delete = models.SET_NULL, blank = True, null = True, default = None)
    next_block = models.ForeignKey(TypeBlock, verbose_name = 'Следующий блок', null = True, blank = True, on_delete = models.SET_NULL)
    delay = models.IntegerField(verbose_name = 'Задержка перед реакцией (секунды)', default = 0)
    conditions = models.ManyToManyField(Condition, verbose_name = 'Условия', blank = True)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
    
    def __str__(self):
        return self.language + ' / ' + self.caption

class FirstTouch(models.Model):
    from_bot = models.ForeignKey(TgBot, verbose_name = 'Через бота', null = True, on_delete = models.CASCADE)
    language = models.CharField(verbose_name = 'Язык перевода', max_length = 5, choices = LANG_CHOICES, default = 'RUS')
    text = models.TextField(verbose_name = 'Текст реакции', blank = True, null = True)
    keyboard = models.ForeignKey(keyboard, verbose_name = 'Клавиатура', on_delete = models.SET_NULL, blank = True, null = True, default = None)
    next_block = models.ForeignKey(TypeBlock, verbose_name = 'Следующий блок', null = True, blank = True, on_delete = models.SET_NULL)
    
    class Meta:
        verbose_name = 'Первое касание'
        verbose_name_plural = 'Первые касания'
    
    def __str__(self):
        return self.text