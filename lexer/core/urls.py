from django.urls import path
from .views import Bot_info, Env_vars

urlpatterns = [
    path('bot/', Bot_info.as_view()),
    path('vars/', Env_vars.as_view()),
]