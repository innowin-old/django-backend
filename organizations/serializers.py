from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer
from .models import (
        Organization,
        StaffCount,
        OrganizationPicture,
        Post,
        Staff,
        Follow,
        Ability,
        Confirmation,
        Customer
    )


class OrganizationSerializer(BaseSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


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


class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


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


class CustomerSerializer(BaseSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }
