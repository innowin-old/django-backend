from base.serializers import BaseSerializer
from .models import Exchange, ExchangeIdentity
from users.models import Identity

# Create Serializers Here
class ExchangeSerilizer(BaseSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['owner'] = identity
        exchange = Exchange.objects.create(**validated_data)
        exchange_identity = ExchangeIdentity(identities_exchange_id=exchange.owner.id, exchanges_identity_id=exchange.id)
        exchange_identity.save()
        return exchange


class ExchangeIdentitySerializer(BaseSerializer):
    class Meta:
        model=ExchangeIdentity
        fields = '__all___'

    def create(self, validated_data):
        request = self.context.get("request")
        identity = Identity.objects.get(identity_user=request.user)
        exchange_identity = ExchangeIdentity.objects.create(**validated_data)
        exchange_identity.identities_exchange = identity
        exchange_identity.save()
        return exchange_identity
