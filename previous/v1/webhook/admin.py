from django.contrib import admin
from .models import Bot_config, User, Partner, UserGroup, RefLink, usr_profile_data

class BotAdmin(admin.ModelAdmin):
    list_display = ('bot_name', 'bot_url', 'webhook_host')
    list_display_links = ('bot_name', 'webhook_host')

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'tg_nickname', 'tg_ID', 'ping_stat', 'additional_info')
    list_display_links = ('name', 'tg_nickname', 'additional_info')
    search_fields = ('name', 'tg_nickname', 'tg_ID')

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('ext_name', 'tg_user', 'rsi_id', 'phone', 'club_status', 'active')
    list_display_links = ('ext_name', 'tg_user')
    search_fields = ('ext_name', 'rsi_id', 'phone', 'club_status', 'active')
    
class UserDataAdmin(admin.ModelAdmin):
    list_display = ('cli_name', 'age_cat_b', 'city', 'invest_value_b', 'business_expirience_b')
    list_filter = ('cli_name', 'age_cat_b', 'city', 'invest_value_b', 'business_expirience_b')
    
admin.site.register(Bot_config, BotAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(usr_profile_data, UserDataAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(UserGroup)
admin.site.register(RefLink)