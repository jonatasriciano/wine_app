
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from allauth.account.views import SignupView

def signup(request):
    """
    Handles user signup. Validates input and creates a new user if valid.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('home')  # Redirect to the home page after signup
            except:
                messages.error(request, 'Username already exists.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'accounts/signup.html')  # Render signup form if GET request


def login_view(request):
    """
    Handles user login by authenticating credentials.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('wine_preferences')  # Redirect to preferences page after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')  # Render login form if GET request


class CustomSignupView(SignupView):
    def get_success_url(self):
        return '/accounts/login/'  # URL para redirecionar após o registro

