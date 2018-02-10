from django.db import models
from django.db.models.signals import post_save

from base.models import Base, BaseManager
from base.signals import update_cache
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
        help_text='Integer',
    )
    message_receiver = models.ForeignKey(
        Identity,
        related_name='message_receivers',
        on_delete=models.CASCADE,
        default=None,
        db_index=True,
        help_text='Integer',
    )
    message_replay = models.ForeignKey(
        'self',
        related_name='replays',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True,
        help_text='Integer',
    )
    message_forward = models.ForeignKey(
        'self',
        related_name='forwards',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_index=True,
        help_text='Integer',
    )
    send_date = models.DateTimeField(auto_now_add=True)
    seen_date = models.DateTimeField(blank=True, null=True, default=None)
    body = models.TextField(blank=True, null=True, default=None, db_index=True, help_text='Text')
    seen = models.BooleanField(default=False, help_text='Boolean')
    message_file = models.ForeignKey(
        Media,
        related_name="message",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        help_text='Integer',
    )

    objects = BaseManager()

# Cache Model Data After Update
post_save.connect(update_cache, sender=Message)