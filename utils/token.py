from datetime import timedelta

from django.contrib.auth.models import User
from django.core.signing import TimestampSigner, SignatureExpired, BadSignature


def generate_token(user):
    signer = TimestampSigner()
    token = signer.sign(user.pk)
    return token


def validate_token(token):
    signer = TimestampSigner()

    # get user id
    try:
        user_id = signer.unsign(token, max_age=timedelta(days=1))
    except SignatureExpired:
        return 'expired-token', None
    except BadSignature:
        return 'invalid-token', None
    # fetch user
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return 'invalid-token', None
    return None, user
