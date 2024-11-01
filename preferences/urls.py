from django.urls import path
from .views import wine_preferences, view_preferences

urlpatterns = [
    path('preferences/', wine_preferences, name='wine_preferences'),  # Para escolher preferências
    path('preferences/view/', view_preferences, name='view_preferences'),  # Para visualizar preferências
]