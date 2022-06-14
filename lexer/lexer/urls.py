"""lexer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import Index
from bearer_auth.views import ObtainToken
from pathlib import Path
import environ, os

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

opt = ''
if env('API_HOST') == 'dev.fountcore.tech': opt = 'lexer/'

urlpatterns = [
    path(opt + '', Index),
    path(opt + 'admin/', admin.site.urls),
    path(opt + 'API_v1/', include('core.urls')),
    path(opt + 'users_api/', include('Users_assets.urls')),
    path(opt + 'content/', include('Content_and_logic.urls')),
    path(opt + 'auth/token', ObtainToken.as_view()),
]
