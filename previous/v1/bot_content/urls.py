from django.urls import path
from .views import get_content, index

urlpatterns = [
    path('', index, name = 'index'),
    path('api/', get_content.as_view())
]