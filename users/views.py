from django.shortcuts import render
from django.core.signing import TimestampSigner, SignatureExpired,\
    BadSignature
from django.contrib.auth.models import User

from datetime import timedelta


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
