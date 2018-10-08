import json

from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from base.views import BaseModelViewSet
from organizations.models import Follow
from users.models import Identity
from .models import Exchange, ExchangeIdentity
from .permissions import IsExchangeOwnerOrReadOnly, IsExchangeFull, IsFirstDefaultExchange, IsAgentOrReadOnly, IsJoinedBefore
from .serializers import ExchangeSerializer, ExchangeIdentitySerializer, ExchangeIdentityListViewSerializer, \
    ExchangeMiniSerializer, ExploreSerializer
from base.models import Post


# Create your views here.
class ExchangeViewSet(BaseModelViewSet):
    """
        A ViewSet for Handle Exchange Views
    """
    permission_classes = [
        IsAuthenticated,
        IsExchangeOwnerOrReadOnly,
        IsFirstDefaultExchange,
        # IsAgentOrReadOnly
    ]

    def get_queryset(self):
        queryset = Exchange.objects.filter(delete_flag=False)

        owner_id = self.request.query_params.get('owner_id')
        if owner_id is not None:
            queryset = queryset.filter(owner_id=owner_id)

        owner_name = self.request.query_params.get('owner_name')
        if owner_name is not None:
            queryset = queryset.filter(owner__name=owner_name)

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
        if self.action in ['list', 'retrieve']:
            return ExchangeMiniSerializer
        return ExchangeSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(
        permission_classes=[IsAuthenticated],
        methods=['get']
    )
    def explore(self, request):
        page = self.request.query_params.get('page', 1)
        limit = self.request.query_params.get('limit', 10)
        identity = Identity.objects.get(identity_user=request.user)
        exchanges = Exchange.objects.filter(delete_flag=False)
        name = self.request.query_params.get('name', None)
        if name is not None:
            exchanges = exchanges.filter(name__contains=name)
        paginator = Paginator(exchanges, limit)
        exchanges = paginator.page(page)
        response = []
        for exchange in exchanges:
            explore = {'exchange': exchange}
            exchange_idenitities = ExchangeIdentity.objects.filter(
                exchange_identity_related_exchange=exchange,
                active_flag=True,
                delete_flag=False
            ).values('exchange_identity_related_identity')
            explore['joint_follows'] = Follow.objects.filter(
                    follow_followed__in=exchange_idenitities,
                    follow_follower=identity,
                    delete_flag=False,
                    follow_accepted=True
                )
            for exchange_idenitity in exchange_idenitities:
                if identity.id == exchange_idenitity['exchange_identity_related_identity']:
                    explore['is_joined'] = True
            exchange_posts = Post.objects.filter(post_parent=exchange)
            explore['supply'] = exchange_posts.filter(post_type='supply').count()
            explore['demand'] = exchange_posts.filter(post_type='demand').count()
            response.append(explore)
        # serial = serializers.serialize('json', response)
        serialize = ExploreSerializer(response, many=True)
        final = {
            'results': serialize.data,
            'count': Exchange.objects.filter(delete_flag=False).count()
        }
        return Response(final, status=status.HTTP_200_OK)

    @list_route(
        permission_classes=[IsAdminUser],
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

    @list_route(methods=['get'], permission_classes=[AllowAny])
    def count(self, request):
        exchange_count = Exchange.objects.all().count()
        return Response({'count': exchange_count}, status=status.HTTP_200_OK)


class ExchangeIdentityViewSet(BaseModelViewSet):
    """
        A ViewSet for Handle Identity Exchange Views
    """
    permission_classes = [IsAuthenticated, IsExchangeFull, IsJoinedBefore]

    def get_queryset(self):
        queryset = ExchangeIdentity.objects.filter(
            delete_flag=False, exchange_identity_related_exchange__delete_flag=False
        )

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

    @list_route(
        methods=['post'],
        permission_classes=[IsAuthenticated]
    )
    def count(self, request):
        exchange_id = request.POST.get('exchange_id', None)
        if exchange_id is not None:
            try:
                exchange = Exchange.objects.get(pk=exchange_id)
            except Exchange.DoesNotExist:
                return Response({"detail": "Exchange Not Found"}, status=status.HTTP_404_NOT_FOUND)
            exchange_count = ExchangeIdentity.objects.filter(exchange_identity_related_exchange=exchange,
                                                             active_flag=True).count()
            return Response({'count': exchange_count}, status=status.HTTP_200_OK)
        return Response({"detail": 'Please Insert Exchange id'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete_flag = True
            instance.save()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
