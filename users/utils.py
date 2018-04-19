from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from utils.token import generate_token


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