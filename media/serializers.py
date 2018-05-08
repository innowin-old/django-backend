import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ModelSerializer, CharField

from .models import Media
from users.models import Identity
from django.contrib.auth.models import User

from .utils import compress_video


class MediaSeriaizer(ModelSerializer):
    file_string = CharField(write_only=True)

    class Meta:
        model = Media
        fields = ('id', 'identity', 'file', 'uploader', 'create_time', 'info', 'delete_flag', 'file_string')

    def create(self, validated_data):
        data = validated_data.pop('file_string')
        request = self.context.get("request")
        
        if 'identity' not in validated_data:
            validated_data['identity'] = Identity.objects.get(identity_user=request.user)

        if request.user.is_superuser and 'uploader' not in validated_data:
            validated_data['uploader'] = User.objects.get(id=request.user.id)

        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        print(ext)
        validated_data['file'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        if ext == 'mp4' or ext == 'avi' or ext == 'webm':
            validated_data['file'] = compress_video(validated_data['file'])
        media = Media.objects.create(**validated_data)
        return media


class MediaMiniSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'info']