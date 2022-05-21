from django.contrib import admin
from .models import EnvVar, TgBot

class Bots(admin.ModelAdmin):
    list_display = ('caption', 'active')

class EnvVarsAdmin(admin.ModelAdmin):
    list_display = ('caption', 'description', 'value')
    
admin.site.register(TgBot, Bots)
admin.site.register(EnvVar, EnvVarsAdmin)