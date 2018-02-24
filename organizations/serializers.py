from base.serializers import BaseSerializer
from .models import (
    Organization,
    StaffCount,
    OrganizationPicture,
    Staff,
    Follow,
    Ability,
    Confirmation,
    Customer
)


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
