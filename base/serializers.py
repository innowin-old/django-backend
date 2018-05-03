from rest_framework.serializers import ModelSerializer
from django.db.models import Q

from users.models import Identity, Profile
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
        self.check_hashtag_profile_strength()
        return instance

    def check_hashtag_profile_strength(self):
        request = self.context.get('request')
        try:
            identity = Identity.objects.filter(identity_user=request.user)
        except Identity.DoesNotExist:
            return False
        hashtags = Hashtag.objects.filter(hashtag_base=identity)
        if hashtags.count() == 3:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                return False
            profile.profile_strength += 10
            profile.save()


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
        if post.post_type == 'post':
            self.check_post_profile_strength()
        else:
            self.check_demand_supply_profile_strength()
        return post

    def check_post_profile_strength(self):
        request = self.context.get('request')
        posts = Post.objects.filter(post_user=request.user, post_type='post')
        if posts.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                return False
            profile.profile_strength += 5
            profile.save()

    def check_demand_supply_profile_strength(self):
        request = self.context.get('request')
        posts = Post.objects.filter(Q(post_user=request.user), Q(post_type='supply') | Q(post_type='demand'))
        if posts.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                return False
            profile.profile_strength += 10
            profile.save()


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