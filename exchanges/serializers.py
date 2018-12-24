from rest_framework import serializers
from base.serializers import BaseSerializer
from organizations.serializers import FollowListSerializer
from .models import Exchange, ExchangeIdentity
from users.models import Identity, Profile, StrengthStates
from users.serializers import IdentityMiniSerializer
from base.models import Post


# Create Serializers Here
class ExchangeSerializer(BaseSerializer):
    supply_count = serializers.SerializerMethodField()
    demand_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Exchange
        exclude = ['child_name']
        extra_kwargs = {
            'owner': {'required': False},
            'updated_time': {'read_only': True}
        }

    def get_supply_count(self, obj):
        return Post.objects.filter(post_parent_id=obj.id, post_type='supply').count()

    def get_demand_count(self, obj):
        return Post.objects.filter(post_parent_id=obj.id, post_type='demand').count()

    def get_post_count(self, obj):
        return Post.objects.filter(post_parent_id=obj.id, post_type='post').count()

    def create(self, validated_data):
        request = self.context.get("request")
        if 'owner' not in validated_data:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['owner'] = identity
        if not request.user.is_superuser:
            validated_data['members_count'] = 100
            validated_data['is_default_exchange'] = False
        exchange = Exchange.objects.create(**validated_data)
        exchange_identity = ExchangeIdentity(exchange_identity_related_identity_id=exchange.owner_id,
                                             exchange_identity_related_exchange_id=exchange.id)
        exchange_identity.save()
        return exchange


class ExchangeMiniSerializer(BaseSerializer):
    supply_count = serializers.SerializerMethodField()
    demand_count = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Exchange
        depth = 1
        exclude = ['created_time', 'updated_time', 'delete_flag', 'active_flag', 'child_name']

    def get_supply_count(self, obj):
        return Post.objects.filter(post_parent_id=obj.id, post_type='supply').count()

    def get_demand_count(self, obj):
        return Post.objects.filter(post_parent_id=obj.id, post_type='demand').count()

    def get_post_count(self, obj):
        return Post.objects.filter(post_parent_id=obj.id, post_type='post').count()


class ExchangeIdentityListViewSerializer(BaseSerializer):
    exchange_identity_related_exchange = ExchangeMiniSerializer()
    exchange_identity_related_identity = IdentityMiniSerializer()

    class Meta:
        depth = 1
        model = ExchangeIdentity
        exclude = ['updated_time', 'child_name']


class ExchangeIdentitySerializer(BaseSerializer):
    class Meta:
        model = ExchangeIdentity
        exclude = ['child_name']
        extra_kwargs = {
            'exchange_identity_related_identity': {'required': False},
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if 'exchange_identity_related_identity' not in validated_data:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['exchange_identity_related_identity'] = identity
        else:
            identity = Identity.objects.get(pk=validated_data['exchange_identity_related_identity'])
        exchange_identity = ExchangeIdentity.objects.create(**validated_data)
        exchange_identity.save()
        if identity.identity_user is not None:
            self.check_exchange_identity_profile_strength(identity)
        return exchange_identity

    def check_exchange_identity_profile_strength(self, identity):
        request = self.context.get("request")
        exchange_identity = ExchangeIdentity.objects.filter(exchange_identity_related_identity=identity)
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.exchange_obtained is False and exchange_identity.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=request.user)
            profile.profile_strength += 5
            profile.save()
            user_strength.exchange_obtained = True


class ExploreSerializer(serializers.Serializer):
    exchange = ExchangeMiniSerializer()
    joint_follows = FollowListSerializer(many=True)
    is_joined = serializers.BooleanField(default=False)
    supply = serializers.IntegerField(default=0)
    demand = serializers.IntegerField(default=0)