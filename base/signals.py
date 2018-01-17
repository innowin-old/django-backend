from django.core.cache import cache
from django.conf import settings


def update_cache(sender, instance, **kwargs):
    cache.set(instance._meta.db_table, sender.objects.filter(delete_flag=False), settings.CACHE_TIMEOUT)
