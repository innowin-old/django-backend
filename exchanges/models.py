from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

from users.models import Identity
from base.models import Base, Hashtag, BaseManager
from base.signals import update_cache, set_child_name
from media.models import Media


# Create your models here.
class Exchange(Base):
    owner = models.ForeignKey(Identity, related_name='exchanges', db_index=True, on_delete=models.CASCADE,
                              help_text='Integer')
    name = models.CharField(max_length=32, validators=[MinLengthValidator(2)], db_index=True, help_text='String(30)')
    exchange_image = models.ForeignKey(
        Media,
        related_name="exchange",
        blank=True,
        null=True,
        help_text='Integer',
    )
    exchange_banner = models.ForeignKey(
        Media,
        related_name="exchange_banner",
        blank=True,
        null=True,
        help_text="Integer",
        db_index=True,
    )
    link = models.URLField(blank=True, help_text='Url', db_index=True)
    description = models.TextField(
        max_length=100,
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
    private = models.BooleanField(default=False, help_text='Boolean', db_index=True)
    members_count = models.BigIntegerField(default=100, help_text='BigInteger', db_index=True)
    is_default_exchange = models.BooleanField(default=False, help_text='Boolean', db_index=True)
    active_flag = models.BooleanField(default=True, help_text='Boolean', db_index=True)
    supply_count = models.IntegerField(default=0)
    demand_count = models.IntegerField(default=0)
    post_count = models.IntegerField(default=0)

    objects = BaseManager()

    def __str__(self):
        return str(self.pk) + ': ' + self.name


# Cache Model Data After Update
post_save.connect(update_cache, sender=Exchange)
# Set Child Name
pre_save.connect(set_child_name, sender=Exchange)


class ExchangeIdentity(Base):
    JOIN_TYPES = (
        ('join', 'عضو'),
        ('quest', 'مهمان'),
        ('admin', 'ادمین'),
    )
    exchange_identity_related_exchange = models.ForeignKey(
        Exchange,
        related_name="identities_exchange",
        help_text='Integer',
        on_delete=models.CASCADE,
        db_index=True
    )
    exchange_identity_related_identity = models.ForeignKey(
        Identity,
        related_name="exchanges_identities",
        help_text='Integer',
        on_delete=models.CASCADE,
        db_index=True,
    )
    join_type = models.CharField(
        choices=JOIN_TYPES,
        max_length=10,
        default='join',
        help_text='join | quest',
        db_index=True,
    )
    active_flag = models.BooleanField(default=True, help_text='Boolean', db_index=True)
    indicator_flag = models.BooleanField(default=False, db_index=True)

    objects = BaseManager()


# Cache Model Data After Update
post_save.connect(update_cache, sender=ExchangeIdentity)
# Set Child Name
pre_save.connect(set_child_name, sender=ExchangeIdentity)
