from django.db import models

from base.models import Base
from users.models import Identity
from media.models import Media

# Create your models here.
class Message(Base):
    message_sender = models.ForeignKey(
        Identity,
        related_name='messages_sender',
        on_delete=models.CASCADE,
        default=None,
        db_index=True,
    )
    message_receiver = models.ForeignKey(
        Identity,
        related_name='message_receivers',
        on_delete=models.CASCADE,
        default=None,
        db_index=True,
    )
    message_replay = models.ForeignKey(
        'self',
        related_name='replays',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True,
    )
    message_forward = models.ForeignKey(
        'self',
        related_name='forwards',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True,
    )
    send_date = models.DateTimeField(auto_now_add=True)
    seen_date = models.DateTimeField(blank=True, null=True, default=None)
    body = models.TextField(blank=True, null=True, default=None, db_index=True)
    seen = models.BooleanField(default=False)
    message_file = models.ForeignKey(
        Media,
        related_name="message",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
    )