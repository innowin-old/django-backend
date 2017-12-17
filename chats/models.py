from datetime import datetime

from django.db import models

from users.models import Identity

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(
        Identity,
        related_name='messages_sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Identity,
        related_name='message_receivers',
        on_delete=models.CASCADE
    )
    replay = models.ForeignKey(
        'self',
        related_name='replays',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    forward = models.ForeignKey(
        'self',
        related_name='forwards',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    forward_from = models.ForeignKey(
        Identity,
        related_name='forwarded_from',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    send_date = models.DateTimeField(default=datetime.now())
    seen_date = models.DateTimeField(blank=True, null=True)
    body = models.TextField()
    seen = models.BooleanField(default=False)