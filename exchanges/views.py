import json

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import list_route
from rest_framework.response import Response

from base.views import BaseModelViewSet
from .models import Exchange, ExchangeIdentity
from .permissions import IsExchangeOwnerOrReadOnly, IsExchangeFull, IsAgentOrReadOnly
from .serializers import ExchangeSerializer, ExchangeIdentitySerializer, ExchangeIdentityListViewSerializer


# Create your views here.
class ExchangeViewSet(BaseModelViewSet):
    """
        A ViewSet for Handle Exchange Views
    """
    # queryset = Exchange.objects.all()
    permission_classes = [IsAgentOrReadOnly, IsExchangeOwnerOrReadOnly, IsAuthenticated]

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
        if private is not None:
            queryset = queryset.filter(private=private)

        member_count = self.request.query_params.get('member_count', None)
        if member_count is not None:
            queryset = queryset.filter(member_count=member_count)

        active_flag = self.request.query_params.get('active', None)
        if active_flag is not None:
            queryset = queryset.filter(active_flag=active_flag)

        return queryset

    def get_serializer_class(self):
        return ExchangeSerializer

    @list_route(
        permission_classes=[AllowAny],
        methods=['post']
    )
    def import_exchanges(self, request):
        jsonString = request.data.get('records', None)
        data = json.loads(jsonString)
        errors = []
        for record in data:
            try:
                exchange = Exchange.objects.create(
                    name=record.get('name', None),
                    link=record.get('link', None),
                    description=record.get('description', None),
                    private=record.get('private', None),
                    members_count=record.get('members_count', None),
                    active_flag=record.get('active_flag', None),
                    owner_id=record.get('owner', None),
                    exchange_image=record.get('exchange_image', None),
                    exchange_hashtag=record.get('exchange_hashtag', None)
                )
            except Exception as e:
                errors.append({
                    'data': record,
                    'status': str(e)
                })
        response = {
            'errors': errors
        }
        return Response(response)


class ExchangeIdentityViewSet(BaseModelViewSet):
    """
        A ViewSet for Handle Identity Exchange Views
    """
    # queryset = ExchangeIdentity.objects.all()
    permission_classes = [IsAuthenticated, IsExchangeFull]

    def get_queryset(self):
        queryset = ExchangeIdentity.objects.all()

        exchange_id = self.request.query_params.get('exchange_id', None)
        if exchange_id is not None:
            queryset = queryset.filter(exchange_identity_related_exchange_id=exchange_id)

        exchange_name = self.request.query_params.get('exchange_name', None)
        if exchange_name is not None:
            queryset = queryset.filter(exchange_identity_related_exchange__name__contains=exchange_name)

        identity_id = self.request.query_params.get('identity_id', None)
        if identity_id is not None:
            queryset = queryset.filter(exchange_identity_related_identity_id=identity_id)

        identity_name = self.request.query_params.get('identity_name', None)
        if identity_name is not None:
            queryset = queryset.filter(exchange_identity_related_identity__name__contains=identity_name)

        join_type = self.request.query_params.get('join_type', None)
        if join_type is not None:
            queryset = queryset.filter(join_type=join_type)

        active_flag = self.request.query_params.get('active_flag', None)
        if active_flag is not None:
            queryset = queryset.filter(active_flag=active_flag)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ExchangeIdentityListViewSerializer
        return ExchangeIdentitySerializer
