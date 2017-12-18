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


class HashtagParent(models.Model):
    title = models.CharField(db_index=True, max_length=50)


class Hashtag(models.Model):
    title = models.CharField(db_index=True, max_length=50)
    related_parent = models.ForeignKey(HashtagParent, related_name='nested_mentions', blank=True, null=True)
    c_type = models.ForeignKey(ContentType, related_name='content_type_mention',null=True,blank=True)
    related_instance_id = models.PositiveIntegerField()
    content_instance = GenericForeignKey('c_type', 'related_instance_id')
    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)
