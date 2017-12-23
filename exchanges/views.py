from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .models import Exchange, Exchange_Identity
from .serializers import ExchangeSerilizer, ExchangeIdentitySerializer

# Create your views here.
class ExchangeViewSet(ModelViewSet):
    """
        A ViewSet for Handle Exchange Views
    """
    queryset = Exchange.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Exchange.objects.all()

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

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
    queryset = Exchange_Identity.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Exchange_Identity.objects.all()

        exchanges_identity_id = self.request.query_params.get('exchange_id', None)
        if exchanges_identity_id is not  None:
            queryset = queryset.filter(exchanges_identity_id=exchanges_identity_id)

        identities_exchange_id = self.request.query_params.get('identity_id', None)
        if identities_exchange_id is not None:
            queryset = queryset.filter(identities_exchange_id=identities_exchange_id)

        join_type = self.request.query_params.get('join_type', None)
        if join_type is not None:
            queryset = queryset.filter(join_type=join_type)

        active_flag = self.request.query_params.get('active_flag', None)
        if active_flag is not None:
            queryset = queryset.filter(active_flag=active_flag)

        return queryset

    def get_serializer_class(self):
        return ExchangeIdentitySerializer