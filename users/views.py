from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.signing import TimestampSigner, SignatureExpired,\
    BadSignature

from datetime import timedelta


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


def active_user(request, token):
    signer = TimestampSigner()

    # get user id
    try:
        user_id = signer.unsign(token, max_age=timedelta(days=1))
    except SignatureExpired:
        context = {
            'msg': 'Token was Expired',
        }
        return render(request, 'activation.html', context)
    except BadSignature:
        context = {
            'msg': 'Token does not Match',
        }
        return render(request, 'activation.html', context)

    # fetch user
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        context = {
            'msg': 'User Does Not Exist',
        }
        return render(request, 'activation.html', context)

    # active user
    user.is_active = True
    user.save()

    context = {
        'msg': 'User Actived Successfully',
    }
    return render(request, 'activation.html', context)
