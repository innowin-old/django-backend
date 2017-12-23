from rest_framework.serializers import ModelSerializer

from .models import Exchange, Exchange_Identity

# Create Serializers Here
class ExchangeSerilizer(ModelSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'


class ExchangeIdentitySerializer(ModelSerializer):
    class Meta:
        model=Exchange_Identity
        fields = '__all___'