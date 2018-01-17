import os

from django.conf import settings
from sendfile import sendfile


def serve(request, name):
    file_path = os.path.join(settings.SENDFILE_ROOT, 'media', os.path.basename(name))
    p, ext = os.path.splitext(name)
    if ext in ['.jpg', '.png']:
        return sendfile(request, file_path)
    return sendfile(request, file_path, attachment=True)
