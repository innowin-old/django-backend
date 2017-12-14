from rest_framework.serializers import ModelSerializer
from .models import (
        Organization,
        StaffCount,
        Picture
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
