from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Exchange, ExchangeIdentity
from .permissions import IsExchangeOwnerOrReadOnly, IsExchangeIdentity
from .serializers import ExchangeSerilizer, ExchangeIdentitySerializer

# Create your views here.
class ExchangeViewSet(ModelViewSet):
    """
        A ViewSet for Handle Exchange Views
    """
    # queryset = Exchange.objects.all()
    permission_classes = [IsExchangeOwnerOrReadOnly, IsAuthenticated]

    def get_queryset(self):
        queryset = Exchange.objects.all()

        owner_id = self.request.query_params.get('owner_id')
        if owner_id is not None:
            queryset = queryset.filter(owner_id=owner_id)

        owner_name = self.request.query_params.get('owner_name')
        if owner_name is not None:
            queryset = queryset.filter(owner__name__contains=owner_name)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)

        description = self.request.query_params.get('description', None)
        if description is not None:
            queryset = queryset.filter(description=description)

        hashtag_id = self.request.query_params.get('exchange_hashtag', None)
        if hashtag_id is not None:
            queryset = queryset.filter(hashtag_id=hashtag_id)

        hashtag_title = self.request.query_params.get('exchange_hashtag_name', None)
        if hashtag_title is not None:
            queryset = queryset.filter(hashtag__title=hashtag_title)

        private = self.request.query_params.get('private', None)
        if private is not  None:
            queryset = queryset.filter(private=private)

        member_count = self.request.query_params.get('member_count', None)
        if member_count is not None:
            queryset = queryset.filter(member_count=member_count)

        active_flag = self.request.query_params.get('active', None)
        if active_flag is not None:
            queryset = queryset.filter(active_flag=active_flag)

        return queryset

    def get_serializer_class(self):
        return ExchangeSerilizer


class ExchangeIdentityViewSet(ModelViewSet):
    """
        A ViewSet for Handle Identity Exchange Views
    """
    # queryset = ExchangeIdentity.objects.all()
    permission_classes = [IsAuthenticated, IsExchangeIdentity]

    def get_queryset(self):
        queryset = ExchangeIdentity.objects.all()

        exchange_id = self.request.query_params.get('exchange_id', None)
        if exchange_id is not  None:
            queryset = queryset.filter(exchanges_identity_id=exchange_id)

        exchange_name = self.request.query_params.get('exchange_name', None)
        if exchange_name is not  None:
            queryset = queryset.filter(exchanges_identity__name__contains=exchange_name)

        identity_id = self.request.query_params.get('identity_id', None)
        if identity_id is not None:
            queryset = queryset.filter(identities_exchange_id=identity_id)

        identity_name = self.request.query_params.get('identity_name', None)
        if identity_name is not None:
            queryset = queryset.filter(identities_exchange__name__contains=identity_name)

        join_type = self.request.query_params.get('join_type', None)
        if join_type is not None:
            queryset = queryset.filter(join_type=join_type)

        active_flag = self.request.query_params.get('active_flag', None)
        if active_flag is not None:
            queryset = queryset.filter(active_flag=active_flag)

        return queryset

    def get_serializer_class(self):
        return ExchangeIdentitySerializer