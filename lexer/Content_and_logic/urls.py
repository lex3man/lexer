from django.urls import path
from .views import Get_content

urlpatterns = [
    path('', Get_content.as_view())
]