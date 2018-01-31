import os

from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from sendfile import sendfile

from base.permissions import IsOwnerOrReadOnly
from .serializers import MediaSeriaizer
from .models import Media


class MediaViewSet(ModelViewSet):
    """
        A ViewSet for Handle Media Views
    """
    #queryset = Media.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        return MediaSeriaizer

    def get_queryset(self):
        queryset = Media.objects.all()
        return queryset


def serve(request, name):
    file_path = os.path.join(settings.SENDFILE_ROOT, 'media', os.path.basename(name))
    p, ext = os.path.splitext(name)
    if ext in ['.jpg', '.png']:
        return sendfile(request, file_path)
    return sendfile(request, file_path, attachment=True)
