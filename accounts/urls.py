from django.urls import path
from allauth.account.views import LoginView, LogoutView, SignupView

urlpatterns = [
    path('login/', LoginView.as_view(), name='account_login'),  # Página de login
    path('logout/', LogoutView.as_view(), name='account_logout'),  # Página de logout
    path('signup/', SignupView.as_view(), name='account_signup'),  # Página de signup
]