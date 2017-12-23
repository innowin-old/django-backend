from django.db import models

from base.models import Base, Hashtag
from media.models import Media
from users.models import Identity


# Create your models here.
class Exchange(Base):
    name = models.CharField(max_length=30)
    exchange_image = models.ForeignKey(
        Media,
        related_name="exchange",
        blank=True,
        null=True,
    )
    link = models.URLField(blank=True)
    description = models.TextField(
        max_length=300,
        blank=True
    )
    exchange_hashtag = models.ForeignKey(
        Hashtag,
        related_name="exchange",
        blank=True,
        null=True,
    )
    private = models.BooleanField(default=False)
    members_count = models.IntegerField(default=100)


class Exchange_Identity(Base):
    JOIN_TYPES = (
        ('join', 'عضو'),
        ('quest', 'مهمان'),
    )
    exchanges_identity = models.ForeignKey(
        Exchange,
        related_name="identities"
    )
    identities_exchange = models.ForeignKey(
        Identity,
        related_name="exchanges"
    )
    join_type = models.CharField(
        choices=JOIN_TYPES,
        max_length=10,
        default='join',
    )
    active_flag = models.BooleanField(default=True)