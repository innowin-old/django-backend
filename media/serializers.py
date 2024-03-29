import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ModelSerializer, CharField

from .models import Media
from users.models import Identity
from django.contrib.auth.models import User
from base.models import Base

from .utils import compress_video, compress_image, set_files_count


class MediaSeriaizer(ModelSerializer):
    file_string = CharField(write_only=True)
    file_usage = CharField(write_only=True, required=False)

    class Meta:
        model = Media
        fields = ('id', 'file_related_parent', 'identity', 'file', 'uploader', 'create_time', 'info', 'delete_flag', 'file_string', 'file_usage')

    def create(self, validated_data):
        data = validated_data.pop('file_string')
        request = self.context.get("request")

        if 'identity' not in validated_data:
            validated_data['identity'] = Identity.objects.get(identity_user=request.user)

        if request.user.is_superuser and 'uploader' not in validated_data:
            validated_data['uploader'] = User.objects.get(id=request.user.id)

        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        validated_data['file'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        if ext == 'mp4' or ext == 'avi' or ext == 'webm':
            validated_data['file'] = compress_video(validated_data['file'])
        elif ext == 'jpeg' or ext == 'png':
            validated_data['file'] = compress_image(image=validated_data['file'], usage=validated_data.get('file_usage'))
        if 'file_usage' in validated_data:
            validated_data.pop('file_usage')
        media = Media.objects.create(**validated_data)
        if validated_data.get('file_related_parent', '') != '':
            set_files_count(validated_data.get('file_related_parent', 0))
        return media


class MediaMiniSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'info']
