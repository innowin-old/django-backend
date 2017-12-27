from djagno.core.cache import cache
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models. import Base
from organizations.models import Organization

def update_cache(sender, instance, **kwargs):
    cache.set(instance._meta.db_table, sender.objects.filter(delete_flag=False), settings.CACHE_TIMEOUT)

post_save.connect(update_cache, sender=Organization)
