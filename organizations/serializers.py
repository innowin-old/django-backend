from rest_framework.serializers import ModelSerializer
from .models import (
        Organization,
        StaffCount,
        Picture,
        Post,
        Staff,
        Follow,
        Ability,
        Confirmation,
        Customer
    )


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class StaffCountSerializer(ModelSerializer):
    class Meta:
        model = StaffCount
        fields = '__all__'


class PictureSerializer(ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class AbilitySerializer(ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'


class ConfirmationSerializer(ModelSerializer):
    class Meta:
        model = Confirmation
        fields = '__all__'


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
