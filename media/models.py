import os
import uuid
from os.path import basename

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

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
        db_index=True)
    file = models.FileField(
        upload_to=get_upload_path,
        storage=media_file_storage)
    uploader = models.ForeignKey(User, related_name="medias",
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 db_index=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return basename(self.file.file.name)
