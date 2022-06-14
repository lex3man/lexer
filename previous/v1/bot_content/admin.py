from django.contrib import admin
from .models import start_content, keyboard, keyboard_button, social_link, links_group, main_menu_reaction, state

class KBAdmin(admin.ModelAdmin):
    list_display = ('caption', 'name', 'language')
    list_display_links = ('caption', 'name')

class KBBAdmin(admin.ModelAdmin):
    list_display = ('caption', 'text', 'order', 'visibls_for')
    list_display_links = ('caption', 'order')
    search_fields = ('caption', 'text')

class SLAdmin(admin.ModelAdmin):
    list_display = ('link_name', 'social')
    list_display_links = ('link_name', 'social')

class LGAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'permition_class')
    list_display_links = ('group_name', 'permition_class')

class StateAdmin(admin.ModelAdmin):
    list_display = ('caption', 'name', 'state_id')
    list_display_links = ('caption', 'name')
    search_fields = ('caption', 'state_id', 'name')

admin.site.register(start_content)
admin.site.register(keyboard, KBAdmin)
admin.site.register(keyboard_button, KBBAdmin)
admin.site.register(social_link, SLAdmin)
admin.site.register(links_group, LGAdmin)
admin.site.register(main_menu_reaction)
admin.site.register(state, StateAdmin)
