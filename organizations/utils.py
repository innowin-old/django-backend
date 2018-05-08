from base.serializers import BaseSerializer
from .models import Organization


class OrganizationListSerializer(BaseSerializer):
    class Meta:
        model = Organization
        fields = ('owner', 'username', 'email', 'official_name', 'ownership_type', 'business_type')
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }