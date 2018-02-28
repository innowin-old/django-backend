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
from users.serializers import UserMiniSerializer, IdentityMiniSerializer


class OrganizationSerializer(BaseSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get('request')
        if not request.user.is_superuser or 'owner' not in validated_data:
            validated_data['owner'] = request.user
        organization = Organization.objects.create(**validated_data)
        return organization

class OrganizationListViewSerializer(BaseSerializer):
    owner = UserMiniSerializer()

    class Meta:
        model = Organization
        fields = ['id', 'owner', 'admins', 'username', 'email', 'nike_name', 'official_name', 'national_code']


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
