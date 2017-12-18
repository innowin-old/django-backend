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
            'related_parent': {'read_only': True},
            'hashtag_base': {'read_only': True},
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        instance = Hashtag.objects.create(**validated_data)
        if HashtagParent.objects.filter(title=validated_data['title']).count() == 0:
            parent_instance = HashtagParent.objects.create(title=validated_data['title'])
        else:
            parent_instance = HashtagParent.objects.get(title=validated_data['title'])
        instance.related_parent = parent_instance
        instance.save()
        return instance
