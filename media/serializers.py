import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ModelSerializer, CharField

from .models import Media
from users.models import Identity


class MediaSeriaizer(ModelSerializer):
    file_string = CharField(write_only=True)

    class Meta:
        model = Media
        fields = ('identity', 'file', 'uploader', 'create_time', 'info', 'delete_flag', 'file_string')

    def create(self, validated_data):
        data = validated_data.pop('file_string')
        request = self.context.get("request")
        identity = Identity.objects.get(identity_user=request.user)
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        validated_data['file'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        media = Media.objects.create(**validated_data, identity=identity)
        return media