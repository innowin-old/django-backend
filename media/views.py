import os

from django.conf import settings
from sendfile import sendfile


def serve(request, name):
    file_path = os.path.join(settings.SENDFILE_ROOT, 'media', os.path.basename(name))
    return sendfile(request, file_path)
