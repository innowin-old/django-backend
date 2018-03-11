import os
import uuid
import json
from os.path import basename

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from base.models import BaseManager
from base.signals import update_cache
from media.MediaStorage import MediaStorage


def get_upload_path(media, filename):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    return os.path.join(settings.MEDIA_DIR, uuid.uuid4().hex + ext)


media_file_storage = MediaStorage(location=settings.MEDIA_DIR)


class Media(models.Model):
    identity = models.ForeignKey(
        'users.Identity',
        related_name="identity_medias",
        on_delete=models.CASCADE,
        db_index=True,
        blank=True,
        null=True
    )
    file = models.FileField(
        upload_to=get_upload_path,
        storage=media_file_storage,
        blank=True,
        null=True,
    )
    uploader = models.ForeignKey(User, related_name="medias",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)
    info = models.TextField(default='{}')
    delete_flag = models.BooleanField(db_index=True, default=False)

    objects = BaseManager()

    def __str__(self):
        return basename(self.file.file.name)


# Cache Model Data After Update
post_save.connect(update_cache, sender=Media)


def update_meta(sender, instance, **kwargs):
    post_save.disconnect(update_meta, sender=Media)
    data = {'size': os.path.getsize(instance.file.path)}
    instance.info = json.dumps(data)
    instance.save()
    post_save.connect(update_meta, sender=Media)


post_save.connect(update_meta, sender=Media)
