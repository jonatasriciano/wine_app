from django.shortcuts import redirect

def home(request):
    """
    Redirects to the login page or preferences page if logged in.
    """
    if request.user.is_authenticated:
        return redirect('view_preferences')  # Redireciona para a página de preferências
    return redirect('account_login')  # Redireciona para a página de login