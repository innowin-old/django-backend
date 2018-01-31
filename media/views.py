import os

from django.conf import settings

from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated

from sendfile import sendfile

from base.permissions import IsOwnerOrReadOnly
from .serializers import MediaSeriaizer
from .models import Media


class MediaViewSet(ModelSerializer):
    """
        A ViewSet for Handle Media Views
    """
    queryset = Media.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        return MediaSeriaizer


def serve(request, name):
    file_path = os.path.join(settings.SENDFILE_ROOT, 'media', os.path.basename(name))
    p, ext = os.path.splitext(name)
    if ext in ['.jpg', '.png']:
        return sendfile(request, file_path)
    return sendfile(request, file_path, attachment=True)
