from base.serializers import BaseSerializer
from .models import Exchange, ExchangeIdentity
from users.models import Identity


# Create Serializers Here
class ExchangeSerializer(BaseSerializer):
    class Meta:
        model = Exchange
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        if 'owner' not in validated_data:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['owner'] = identity
        exchange = Exchange.objects.create(**validated_data)
        exchange_identity = ExchangeIdentity(exchange_identity_related_identity_id=exchange.owner_id,
                                             exchange_identity_related_exchange_id=exchange.id)
        exchange_identity.save()
        return exchange


class ExchangeMiniSerializer(BaseSerializer):
    class Meta:
        model = Exchange
        exclude = ['created_time', 'updated_time', 'delete_flag', 'active_flag']


class ExchangeIdentityListViewSerializer(BaseSerializer):
    exchange_identity_related_exchange = ExchangeMiniSerializer()

    class Meta:
        model = ExchangeIdentity
        exclude = ['updated_time']


class ExchangeIdentitySerializer(BaseSerializer):
    class Meta:
        model = ExchangeIdentity
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        if not request.user.is_superuser:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['exchange_identity_related_identity'] = identity
        elif request.user.is_superuser:
            if 'exchange_identity_related_identity' not in validated_data:
                identity = Identity.objects.get(identity_user=request.user)
                validated_data['exchange_identity_related_identity'] = identity
        exchange_identity = ExchangeIdentity.objects.create(**validated_data)
        exchange_identity.save()
        return exchange_identity