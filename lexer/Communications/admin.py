from django.contrib import admin
from .models import Sending, MessageHistory

class SendingAdmin(admin.ModelAdmin):
    list_display = ('sending_id', 'create_time', 'sending_time', 'sending_text', 'send_done')

admin.site.register(Sending, SendingAdmin)
admin.site.register(MessageHistory)
