from rest_framework.serializers import ModelSerializer
from .models import (
    Base,
    HashtagParent,
    Hashtag,
    BaseComment,
    Post,
    BaseCertificate,
    BaseRoll,
    RollPermission
)


class BaseSerializer(ModelSerializer):
    class Meta:
        model = Base
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class HashtagParentSerializer(BaseSerializer):
    class Meta:
        model = HashtagParent
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class HashtagSerializer(BaseSerializer):
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


class BaseCommentSerializer(BaseSerializer):
    class Meta:
        model = BaseComment
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'post_user': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        post = Post.objects.create(**validated_data, post_user=request.user)
        post.save()
        return post


class CertificateSerializer(BaseSerializer):
    class Meta:
        model = BaseCertificate
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class RollSerializer(BaseSerializer):
    class Meta:
        model = BaseRoll
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class RollPermissionSerializer(BaseSerializer):
    class Meta:
        model = RollPermission
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }