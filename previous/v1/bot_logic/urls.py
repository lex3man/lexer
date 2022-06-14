from django.urls import path
from .views import MessageLogging, CreateSending, SendingSend

urlpatterns = [
    path('updates/', MessageLogging.as_view()),
    path('create_sending/', CreateSending.as_view()),
    path('sent/', SendingSend.as_view())
]