from django.core.cache import cache
from django.conf import settings


def update_cache(sender, instance, **kwargs):
    cache.set(instance._meta.db_table, sender.objects.filter(delete_flag=False), settings.CACHE_TIMEOUT)


def set_child_name(sender, instance, **kwargs):
    print(instance._meta.model_name)
    instance.child_name = instance._meta.model_name
