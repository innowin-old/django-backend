from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")


def login_page(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(settings.SOCIAL_AUTH_LOGIN_REDIRECT_URL)
        return redirect(settings.SOCIAL_AUTH_LOGIN_ERROR_URL)
    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    return redirect('/#/auth/logout/')
