from django.urls import path
from .views import wine_preferences, view_preferences

urlpatterns = [
    path('', wine_preferences, name='wine_preferences'),  # This could also be 'preferences/'
    path('view/', view_preferences, name='view_preferences'),
]