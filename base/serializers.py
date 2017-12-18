from rest_framework.serializers import ModelSerializer, CharField
from .models import (
        HashtagParent,
        Hashtag
    )


class HashtagParentSerializer(ModelSerializer):
    class Meta:
        model = HashtagParent
        fields = '__all__'


class HashtagSerializer(ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'
        extra_kwargs = {
            'related_parent': {'read_only': True}
        }

    def create(self, validated_data):
        instance = Mention.objects.create(**validated_data)
        parent_instance = Hashtag.objects.create(title=validated_data['title'])
        instance.update(related_parent=parent_instance)
        return instance
