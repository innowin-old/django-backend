from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from utils.token import generate_token

from .models import Identity
from exchanges.models import Exchange, ExchangeIdentity


def send_verification_mail(user):
    link = 'http://daneshboom.ir/users/active/' + generate_token(user) + '/'
    content = render_to_string("activation_email.html", {'user': user, 'link': link})
    msg = EmailMessage(
        subject='verify your account',
        body=content,
        from_email='kamankesh.amr@gmail.com',
        bcc=[user.email]
    )
    msg.content_subtype = "html"
    return msg.send()


def add_user_to_default_exchange(user):
    identity = Identity.objects.get(identity_user=user)
    try:
        exchange = Exchange.objects.get(is_default_exchange=True)
    except Exchange.DoesNotExist:
        exchange = False
    if exchange is not False:
        exchange_identity = ExchangeIdentity.objects.create(exchange_identity_related_identity=identity,
                                                            exchange_identity_related_exchange=exchange,
                                                            join_type='quest')
