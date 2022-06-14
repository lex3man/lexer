from django.contrib import admin
from .models import User, UserTag, Var, RefLink

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'tg_nickname', 'tg_ID', 'ping_stat', 'from_bot')
    search_fields = ('name', 'tg_nickname', 'tg_ID')
    list_filter = ('ping_stat', 'registration_date', 'from_bot', 'tags')
    
class TagAdmin(admin.ModelAdmin):
    list_display = ('caption', 'priority', 'description')

class VarsAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'value')
    search_fields = ('key', 'user', 'value')
    list_filter = ('user', 'key', 'value')

admin.site.register(User, UserAdmin)
admin.site.register(UserTag, TagAdmin)
admin.site.register(Var, VarsAdmin)
admin.site.register(RefLink)
