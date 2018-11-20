from django.contrib.auth.models import User
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
        super_user = User.objects.filter(is_superuser=True).first()
        super_user_identity = Identity.objects.filter(identity_user=super_user)[0]
        exchange = Exchange.objects.create(name='دانش بوم', is_default_exchange=True, owner=super_user_identity)
    if exchange is not False:
        exchange_identity = ExchangeIdentity.objects.create(exchange_identity_related_identity=identity,
                                                            exchange_identity_related_exchange=exchange,
                                                            join_type='quest')


def add_organization_to_default_exchange(organization):
    identity = Identity.objects.get(identity_organization=organization)
    try:
        exchange = Exchange.objects.get(is_default_exchange=True)
    except Exchange.DoesNotExist:
        super_user = User.objects.filter(is_superuser=True).first()
        super_user_identity = Identity.objects.get(identity_user=super_user)
        exchange = Exchange.objects.create(name='دانش بوم', is_default_exchange=True, owner=super_user_identity)
    exchange_identity = ExchangeIdentity.objects.create(exchange_identity_related_identity=identity,
                                                        exchange_identity_related_exchange=exchange,
                                                        join_type='quest')
