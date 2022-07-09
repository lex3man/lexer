from django.contrib import admin
from .models import Sending, MessageHistory

class SendingAdmin(admin.ModelAdmin):
    list_display = ('sending_id', 'create_time', 'sending_time', 'sending_text', 'in_order', 'send_done')
    # readonly_fields = ('in_order', 'send_done')
    search_fields = ('sending_id', 'sending_text', 'sending_time')
    list_filter = ('creator', 'from_bot', 'in_order', 'send_done')
    actions = [Sending.shedule]

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('message_text', 'from_bot', 'user', 'message_time')
    search_fields = ('message_text', 'user', 'message_time')
    list_filter = ('from_bot', 'user')

admin.site.register(Sending, SendingAdmin)
admin.site.register(MessageHistory, HistoryAdmin)
