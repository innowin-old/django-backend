from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)


class HashtagParent(Base):
    title = models.CharField(db_index=True, max_length=50)


class Hashtag(Base):
    title = models.CharField(db_index=True, max_length=50)
    related_parent = models.ForeignKey(HashtagParent, related_name='nested_mentions', blank=True, null=True)
    hashtag_base = models.ForeignKey(Base, related_name='base_hashtags', on_delete=models.CASCADE, blank=True, null=True)
