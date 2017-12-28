from django.db import models
from django.db.models.signals import post_save

from base.models import Base, Hashtag, BaseManager
from base.signals import update_cache
from media.models import Media
from users.models import Identity


# Create your models here.
class Exchange(Base):
    name = models.CharField(max_length=30, db_index=True, help_text='String(30)')
    exchange_image = models.ForeignKey(
        Media,
        related_name="exchange",
        blank=True,
        null=True,
        help_text='Integer',
    )
    link = models.URLField(blank=True, help_text='Url')
    description = models.TextField(
        max_length=300,
        blank=True,
        db_index=True,
        help_text='Integer',
    )
    exchange_hashtag = models.ForeignKey(
        Hashtag,
        related_name="exchange",
        blank=True,
        null=True,
        db_index=True,
        help_text='Integer',
    )
    private = models.BooleanField(default=False, help_text='Boolean')
    members_count = models.IntegerField(default=100, help_text='Boolean')
    active_flag = models.BooleanField(default=True, help_text='Boolean')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=Exchange)


class ExchangeIdentity(Base):
    JOIN_TYPES = (
        ('join', 'عضو'),
        ('quest', 'مهمان'),
    )
    exchanges_identity = models.ForeignKey(
        Exchange,
        related_name="identities",
        help_text='Integer',
    )
    identities_exchange = models.ForeignKey(
        Identity,
        related_name="exchanges",
        help_text='Integer',
    )
    join_type = models.CharField(
        choices=JOIN_TYPES,
        max_length=10,
        default='join',
        help_text='join | quest'
    )
    active_flag = models.BooleanField(default=True, help_text='Boolean')

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=ExchangeIdentity)
