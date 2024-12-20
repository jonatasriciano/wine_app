"""wine_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# Path: /app/wine_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import home  # Importando a nova view


urlpatterns = [
    path('', home, name='home'),  # Adicionando a URL para a raiz
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # Para autenticação
    path('preferences/', include('preferences.urls', namespace='preferences')),  # Para preferências de vinho
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns