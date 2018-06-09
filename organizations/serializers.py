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
from users.models import Identity, Profile, StrengthStates, WorkExperience


class OrganizationSerializer(BaseSerializer):
    class Meta:
        model = Organization
        depth = 1
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if 'owner' not in validated_data or not request.user.is_superuser:
            validated_data['owner'] = request.user
        organization = Organization(**validated_data)
        organization.save()
        return organization


class MetaDataSerializer(BaseSerializer):
    class Meta:
        model = MetaData
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        if validated_data['meta_type'] == 'address':
            identity_meta_data = MetaData.objects.filter(meta_identity=validated_data['meta_identity'],
                                                         meta_type=validated_data['meta_type'])
            if identity_meta_data.count() >= 3:
                error = {'message': "organization have more than 3 " + validated_data['meta_type'] + ' !'}
                raise serializers.ValidationError(error)
            elif len(validated_data['meta_value']) > 100:
                error = {'message': "organization have more than 100 character !"}
                raise serializers.ValidationError(error)
        elif validated_data['meta_type'] == 'address':
            identity_meta_data = MetaData.objects.filter(meta_identity=validated_data['meta_identity'],
                                                         meta_type=validated_data['meta_type'])
            if identity_meta_data.count() >= 4:
                error = {'message': "organization have more than 4 " + validated_data['meta_type'] + ' !'}
                raise serializers.ValidationError(error)
            elif len(validated_data['meta_value']) > 20:
                error = {'message': "organization have more than 20 character !"}
                raise serializers.ValidationError(error)
        meta_data = MetaData.objects.create(**validated_data)
        meta_data.save()
        return meta_data


class MetaDataField(serializers.Field):

    def to_representation(self, obj):
        ret = []
        meta_data = MetaData.objects.filter(meta_organization_id=obj.id)
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
        fields = ['id', 'owner', 'admins', 'username', 'email', 'nike_name', 'official_name', 'national_code',
                  'meta_data']


class StaffCountSerializer(BaseSerializer):
    class Meta:
        model = StaffCount
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class OrganizationPictureSerializer(BaseSerializer):
    class Meta:
        model = OrganizationPicture
        exclude = ['child_name']
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
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class FollowSerializer(BaseSerializer):
    class Meta:
        model = Follow
        exclude = ['child_name']
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
        user = User.objects.get(pk=identity.identity_user_id)
        follows = Follow.objects.filter(follow_follower=identity)
        try:
            user_strength = StrengthStates.objects.get(strength_user=user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=user)
        if user_strength.follow_obtained is False and follows.count() == 3:
            profile = Profile.objects.get(profile_user=user)
            profile.profile_strength += 5
            profile.save()
            user_strength.follow_obtained = True
            user_strength.save()


class AbilitySerializer(BaseSerializer):
    class Meta:
        model = Ability
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class ConfirmationSerializer(BaseSerializer):
    class Meta:
        model = Confirmation
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if 'confirmation_corroborant' not in validated_data or not request.user.is_superuser:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['confirmation_corroborant'] = identity
        if 'confirmation_confirmed' in validated_data:
            validated_data.pop('confirmation_confirmed', None)
        confirmation = Confirmation.objects.create(**validated_data)
        confirmation.save()
        return confirmation

    def update(self, instance, validated_data):
        if 'confirm_flag' in validated_data:
            experience = WorkExperience.objects.get(pk=instance.confirmation_parent_id)
            if validated_data.get('confirm_flag') is True:
                experience.status = "CONFIRMED"
            else:
                experience.status = "WITHOUT_CONFIRM"
            experience.save()
        for key in validated_data:
            setattr(instance, key, validated_data.get(key))
        instance.save()
        return instance


class ConfirmationListViewSerializer(BaseSerializer):
    confirmation_corroborant = IdentityMiniSerializer()
    confirmation_confirmed = IdentityMiniSerializer()

    class Meta:
        model = Confirmation
        exclude = ['updated_time', 'child_name']


class CustomerSerializer(BaseSerializer):
    class Meta:
        model = Customer
        exclude = ['child_name']
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }
