from django.urls import path
from .views import API_hook_config, get_data, add_or_edit_obj

urlpatterns = [
    path('bot_request/', API_hook_config.as_view()),
    path('get_info/', get_data.as_view()),
    path('updates/', add_or_edit_obj.as_view())
]