from rest_framework import serializers
from django.contrib.auth.models import User
from base.serializers import BaseSerializer
from .models import (
    Organization,
    StaffCount,
    OrganizationPicture,
    Staff,
    Follow,
    Ability,
    Confirmation,
    Customer,
    MetaData
)
from users.serializers import UserMiniSerializer, IdentityMiniSerializer
from users.models import Identity, Profile


class OrganizationSerializer(BaseSerializer):

    class Meta:
        model = Organization
        depth = 1
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if 'owner' not in validated_data:
            validated_data['owner'] = request.user
        if not request.user.is_superuser:
            validated_data['owner'] = request.user
        organization = Organization(**validated_data)
        organization.save()
        return organization


class MetaDataSerializer(BaseSerializer):
    class Meta:
        model = MetaData
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class MetaDataField(serializers.Field):

    def to_representation(self, obj):
        ret = []
        try:
            identity = Identity.objects.get(identity_organization_id=obj.id)
        except Identity.DoesNotExist:
            return None
        meta_data = MetaData.objects.filter(meta_identity=identity)
        if meta_data.count() != 0:
            for meta_item in meta_data:
                meta_object = {
                    'id': meta_item.id,
                    'meta_type': meta_item.meta_type,
                    'meta_title': meta_item.meta_title,
                    'meta_value': meta_item.meta_value
                }
                ret.append(meta_object)
        return ret

    def to_internal_value(self, data):
        ret = []
        return ret


class OrganizationListViewSerializer(BaseSerializer):
    owner = UserMiniSerializer()
    meta_data = MetaDataField(source='*', read_only=True)

    class Meta:
        model = Organization
        fields = ['id', 'owner', 'admins', 'username', 'email', 'nike_name', 'official_name', 'national_code', 'meta_data']


class StaffCountSerializer(BaseSerializer):
    class Meta:
        model = StaffCount
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class OrganizationPictureSerializer(BaseSerializer):
    class Meta:
        model = OrganizationPicture
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class StaffListViewSerializer(BaseSerializer):
    staff_user = UserMiniSerializer()

    class Meta:
        model = Staff
        fields = ['id', 'staff_user', 'position', 'staff_organization']


class StaffSerializer(BaseSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class FollowSerializer(BaseSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if (request.user.is_superuser and 'follow_follower' not in validated_data) or not request.user.is_superuser:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['follow_follower'] = identity
        follow = Follow.objects.create(**validated_data)
        follow.save()
        self.check_follow_profile_strength(validated_data['follow_follower'])
        return follow

    def check_follow_profile_strength(self, identity):
        follows = Follow.objects.filter(follow_follower=identity)
        if follows.count() == 3:
            user = User.objects.get(pk=identity.identity_user_id)
            profile = Profile.objects.get(profile_user=user)
            profile.profile_strength += 5
            profile.save()


class AbilitySerializer(BaseSerializer):
    class Meta:
        model = Ability
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class ConfirmationSerializer(BaseSerializer):
    class Meta:
        model = Confirmation
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class ConfirmationListViewSerializer(BaseSerializer):
    confirmation_corroborant = IdentityMiniSerializer()

    class Meta:
        model = Confirmation
        exclude = ['updated_time']


class CustomerSerializer(BaseSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }