from django.db import models
from django.contrib.auth.models import User

from os.path import basename


class Media(models.Model):
    file = models.FileField(upload_to='media/medias')
    uploader = models.ForeignKey(User, related_name="medias",
                                 on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return basename(self.file.file.name)
