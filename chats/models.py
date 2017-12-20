from datetime import datetime

from django.db import models

from users.models import Identity
from media.models import Media

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(
        Identity,
        related_name='messages_sender',
        on_delete=models.CASCADE,
        default=None,
    )
    receiver = models.ForeignKey(
        Identity,
        related_name='message_receivers',
        on_delete=models.CASCADE,
        default=None,
    )
    replay = models.ForeignKey(
        'self',
        related_name='replays',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )
    forward = models.ForeignKey(
        'self',
        related_name='forwards',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )
    send_date = models.DateTimeField(auto_now_add=True)
    seen_date = models.DateTimeField(blank=True, null=True, default=None)
    body = models.TextField(blank=True, null=True, default=None)
    seen = models.BooleanField(default=False)
    file = models.ForeignKey(
        Media,
        related_name="message",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )