from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index(request):
    return render(request, "index.html")


def logout_page(request):
    logout(request)
    return redirect('/#/auth/logout/')
