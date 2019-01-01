from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from django.db.models import Q
from exchanges.models import Exchange

from users.models import Identity, Profile, StrengthStates
from .models import (
    Base,
    HashtagParent,
    Hashtag,
    BaseComment,
    Post,
    BaseCertificate,
    BaseRoll,
    RollPermission,
    HashtagRelation,
    BaseCountry,
    BaseProvince,
    BaseTown,
    BadgeCategory,
    Badge,
    Favorite, FavoriteBase)


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
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class HashtagSerializer(BaseSerializer):
    class Meta:
        model = Hashtag
        exclude = ['child_name']
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
            parent_instance.usage += 1
            parent_instance.save()
        instance.related_parent = parent_instance
        instance.save()
        self.check_hashtag_profile_strength()
        return instance

    def check_hashtag_profile_strength(self):
        request = self.context.get("request")
        try:
            identity = Identity.objects.get(identity_user=request.user)
        except Identity.DoesNotExist:
            identity = Identity.objects.create(identity_user=request.user)
        hashtags = Hashtag.objects.filter(hashtag_base=identity)
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.hashtags_obtained is False and hashtags.count() == 3:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                return False
            profile.profile_strength += 10
            profile.save()
            user_strength.hashtags_obtained = True
            user_strength.save()


class HashtagRelationSerializer(BaseSerializer):
    class Meta:
        model = HashtagRelation
        depth = 1
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class BaseCommentSerializer(BaseSerializer):
    class Meta:
        model = BaseComment
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'comment_sender': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if 'comment_sender' not in validated_data or not request.user.is_superuser:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['comment_sender'] = identity
        comment = BaseComment.objects.create(**validated_data)
        # حال تعداد کامنت های مربوط به هر مدل بیس را در فیلد مربوطه ذخیره می کنیم
        base_instance = Base.objects.filter(id=comment.comment_parent_id)[0]
        base_instance.comments_count = BaseComment.objects.filter(comment_parent_id=base_instance.id).count()
        base_instance.save()
        related_post = Post.objects.filter(id=comment.comment_parent_id)
        if related_post.count() > 0:
            related_post = related_post[0]
            related_exchange = Exchange.objects.filter(id=related_post.post_parent_id)
            if related_exchange.count() > 0:
                related_exchange = related_exchange[0]
                related_exchange_posts = Post.objects.filter(post_parent_id=related_exchange.id)
                comments_count = 0
                for post in related_exchange_posts:
                    comments_count += post.comments_count
                related_exchange.posts_comments_count = comments_count
        return comment


class UserCommentMiniSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class IdentityCommentMiniSerializer(BaseSerializer):
    identity_user = UserCommentMiniSerializer()

    class Meta:
        model = Identity
        depth = 1
        exclude = ['updated_time']


class BaseRepliedCommentSerializer(BaseSerializer):
    comment_sender = IdentityCommentMiniSerializer(read_only=True)

    class Meta:
        model = BaseComment
        exclude = ['child_name']


class BaseCommentListSerializer(BaseSerializer):
    comment_replied = BaseRepliedCommentSerializer(read_only=True)
    comment_sender = IdentityCommentMiniSerializer(read_only=True)

    class Meta:
        model = BaseComment
        depth = 1
        fields = ['id', 'comment_parent', 'comment_sender', 'comment_picture', 'text', 'comment_replied', 'created_time', 'updated_time']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'comment_sender': {'read_only': True}
        }


class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'post_user': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'post_user' not in validated_data:
            validated_data['post_user'] = request.user
        post = Post.objects.create(**validated_data)
        post.save()
        if post.post_parent != None:
            base_parent = Base.objects.filter(id=post.post_parent_id)[0]
            base_parent.posts_count = Post.objects.filter(post_parent_id=post.id).count()
            base_parent.save()
        if post.post_type == 'supply':
            exchange = Exchange.objects.filter(id=post.post_parent_id)
            if exchange.count() > 0:
                exchange = exchange[0]
                exchange.supply_count = Post.objects.filter(post_parent_id=exchange.id, post_type='supply').count()
                exchange.save()
        elif post.post_type == 'demand':
            exchange = Exchange.objects.filter(id=post.post_parent_id)
            if exchange.count() > 0:
                exchange = exchange[0]
                exchange.demand_count = Post.objects.filter(post_parent_id=exchange.id, post_type='demand').count()
                exchange.save()
        elif post.post_type == 'post':
            exchange = Exchange.objects.filter(id=post.post_parent_id)
            if exchange.count() > 0:
                exchange = exchange[0]
                exchange.post_count = Post.objects.filter(post_parent_id=exchange.id, post_type='post').count()
                exchange.save()
        if post.post_type == 'post':
            self.check_post_profile_strength()
        else:
            self.check_demand_supply_profile_strength()
        return post

    def check_post_profile_strength(self):
        request = self.context.get('request')
        posts = Post.objects.filter(post_user=request.user, post_type='post')
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.post_obtained is False and posts.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=request.user)
            profile.profile_strength += 5
            profile.save()
            user_strength.post_obtained = True
            user_strength.save()

    def check_demand_supply_profile_strength(self):
        request = self.context.get('request')
        posts = Post.objects.filter(Q(post_user=request.user), Q(post_type='supply') | Q(post_type='demand'))
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.supply_demand_obtained is False and posts.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=request.user)
            profile.profile_strength += 10
            profile.save()
            user_strength.supply_demand_obtained = True
            user_strength.save()

    @staticmethod
    def validate_post_description(value):
        if len(value) != 0:
            if len(value) < 5:
                error = {'message': "minimum length for post description is 5 character"}
                raise ValidationError(error)
        return value


class PostListSerializer(BaseSerializer):
    class Meta:
        model = Post
        depth = 2
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
            'post_user': {'read_only': True}
        }


class CertificateSerializer(BaseSerializer):
    class Meta:
        model = BaseCertificate
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class CertificateListSerializer(BaseSerializer):
    class Meta:
        model = BaseCertificate
        depth = 1
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class RollSerializer(BaseSerializer):
    class Meta:
        model = BaseRoll
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class RollPermissionSerializer(BaseSerializer):
    class Meta:
        model = RollPermission
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BaseCountrySerializer(BaseSerializer):
    class Meta:
        model = BaseCountry
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BaseProvinceSerializer(BaseSerializer):
    class Meta:
        model = BaseProvince
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BaseTownSerializer(BaseSerializer):
    class Meta:
        model = BaseTown
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BadgeCategorySerializer(BaseSerializer):
    class Meta:
        model = BadgeCategory
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'badge_related_user' not in validated_data:
            validated_data['badge_related_user'] = request.user
        badge_category = BadgeCategory.objects.create(**validated_data)
        return badge_category

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser or 'badge_related_user' not in validated_data:
            validated_data['badge_related_user'] = request.user

        for key in validated_data:
            if key != 'badge_related_user':
                setattr(instance, key, validated_data.get(key, None))

        instance.save()
        return instance


class BadgeCategoryListSerializer(BaseSerializer):
    class Meta:
        model = BadgeCategory
        depth = 1
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class BadgeSerializer(BaseSerializer):
    class Meta:
        model = Badge
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class BadgeListSerializer(BaseSerializer):
    badge_related_badge_category = BadgeCategoryListSerializer()

    class Meta:
        model = Badge
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class FavoriteSerializer(BaseSerializer):
    class Meta:
        model = Favorite
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class FavoriteListSerializer(BaseSerializer):
    class Meta:
        model = Favorite
        depth = 1
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class FavoriteBaseSerializer(BaseSerializer):
    class Meta:
        model = FavoriteBase
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }


class FavoriteBaseListSerializer(BaseSerializer):
    class Meta:
        model = FavoriteBase
        depth = 1
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True},
        }