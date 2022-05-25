from django.urls import path
from .views import CreateUser

urlpatterns = [
    path('new_user/', CreateUser.as_view()),
    path('get_user/', CreateUser.as_view())
]