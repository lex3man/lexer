from django.contrib import admin
from .models import typical_block, text_command, message_history, client_way, sendings

class TBAdmin(admin.ModelAdmin):
    list_display = ('caption', 'language', 'text', 'kb')
    list_display_links = ('caption', 'language')
    search_fields = ('caption', 'language', 'text')

class TCAdmin(admin.ModelAdmin):
    list_display = ('caption', 'text', 'go_to')
    list_display_links = ('caption', 'go_to')
    search_fields = ('caption', 'text')

class MHAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_time', 'msg_text')
    list_display_links = ('user', 'date_time')

class SendingsAdmin(admin.ModelAdmin):
    list_display = ('sending_id', 'sending_list', 'sending_time', 'sending_text', 'send_done')

admin.site.register(typical_block, TBAdmin)
admin.site.register(text_command, TCAdmin)
admin.site.register(sendings, SendingsAdmin)
admin.site.register(message_history, MHAdmin)
admin.site.register(client_way, TBAdmin)
