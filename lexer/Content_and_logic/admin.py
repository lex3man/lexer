from django.contrib import admin
from .models import keyboard_button, keyboard, Command, Condition

class KeyboardButtonsAdmin(admin.ModelAdmin):
    list_display = ('caption', 'text', 'language', 'order', 'from_bot')
    search_fields = ('caption', 'text')
    list_filter = ('language', 'from_bot', 'keyboard')
    
class KeyboardAdmin(admin.ModelAdmin):
    list_display = ('caption', 'name', 'language', 'from_bot')
    list_filter = ('language', 'from_bot')

class CommandAdmin(admin.ModelAdmin):
    list_display = ('caption', 'text', 'language', 'keyboard', 'from_bot')
    search_fields = ('caption', 'text')
    list_filter = ('language', 'from_bot')

admin.site.register(keyboard_button, KeyboardButtonsAdmin)
admin.site.register(keyboard, KeyboardAdmin)
admin.site.register(Command, CommandAdmin)
admin.site.register(Condition)