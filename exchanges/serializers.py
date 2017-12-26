from base.serializers import BaseSerializer
from .models import Exchange, ExchangeIdentity

# Create Serializers Here
class ExchangeSerilizer(BaseSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class ExchangeIdentitySerializer(BaseSerializer):
    class Meta:
        model=ExchangeIdentity
        fields = '__all___'