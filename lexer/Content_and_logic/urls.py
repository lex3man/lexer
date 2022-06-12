from django.urls import path
from .views import Get_content, BotTest

urlpatterns = [
    path('', Get_content.as_view()),
    path('test/', BotTest.as_view())
]