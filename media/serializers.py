import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ModelSerializer, CharField

from .models import Media


class MediaSeriaizer(ModelSerializer):
    file_string = CharField()

    class Meta:
        model = Media
        fields = '__all__'

    def create(self, validated_data):
        data = validated_data['file_string']
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        validated_data['file'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        media = Media.objects.create(**validated_data)
        return media.id