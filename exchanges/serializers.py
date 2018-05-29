from base.serializers import BaseSerializer
from .models import Exchange, ExchangeIdentity
from users.models import Identity, Profile, StrengthStates


# Create Serializers Here
class ExchangeSerializer(BaseSerializer):
    class Meta:
        model = Exchange
        exclude = ['child_name']
        depth = 1
        extra_kwargs = {
            'owner': {'required': False},
            'updated_time': {'read_only': True}
        }

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
        exclude = ['created_time', 'updated_time', 'delete_flag', 'active_flag', 'child_name']


class ExchangeIdentityListViewSerializer(BaseSerializer):
    exchange_identity_related_exchange = ExchangeMiniSerializer()

    class Meta:
        model = ExchangeIdentity
        exclude = ['updated_time', 'child_name']


class ExchangeIdentitySerializer(BaseSerializer):
    class Meta:
        model = ExchangeIdentity
        exclude = ['child_name']
        extra_kwargs = {
            'exchange_identity_related_identity': {'required': False},
            'updated_time': {'read_only': True}
        }

    def create(self, validated_data):
        request = self.context.get("request")
        if 'exchange_identity_related_identity' not in validated_data or not request.user.is_superuser:
            identity = Identity.objects.get(identity_user=request.user)
            validated_data['exchange_identity_related_identity'] = identity
        else:
            identity = Identity.objects.get(pk=validated_data['exchange_identity_related_identity'])
        exchange_identity = ExchangeIdentity.objects.create(**validated_data)
        exchange_identity.save()
        if identity.identity_user is not None:
            self.check_exchange_identity_profile_strength(identity)
        return exchange_identity

    def check_exchange_identity_profile_strength(self, identity):
        request = self.context.get("request")
        exchange_identity = ExchangeIdentity.objects.filter(exchange_identity_related_identity=identity)
        try:
            user_strength = StrengthStates.objects.get(strength_user=request.user)
        except StrengthStates.DoesNotExist:
            user_strength = StrengthStates.objects.create(strength_user=request.user)
        if user_strength.exchange_obtained is False and exchange_identity.count() == 1:
            try:
                profile = Profile.objects.get(profile_user=request.user)
            except Profile.DoesNotExist:
                profile = Profile.objects.create(profile_user=request.user)
            profile.profile_strength += 5
            profile.save()
            user_strength.exchange_obtained = True