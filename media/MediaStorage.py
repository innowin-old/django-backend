import os

from django.core.files.storage import FileSystemStorage
from django.urls import reverse


class MediaStorage(FileSystemStorage):
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(MediaStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name

    def delete(self, name):
        return super(MediaStorage, self).delete(name)

    def url(self, name):
        return reverse('media', kwargs={'name': os.path.basename(name)})
