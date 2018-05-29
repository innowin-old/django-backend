import json
from django.db.models import Q
from django.core import serializers
from rest_framework import status
from rest_framework.decorators import list_route
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from .permissions import (
    IsRollOwnerOrReadOnly,
    IsRollPermissionOwnerOrReadOnly,
    IfExchangeIsAcceptedOrNotAccess,
    IsAdminUserOrReadOnly,
    IsHashtagOwnerOrReadOnly
)

from .models import (
    Base,
    Hashtag,
    HashtagParent,
    BaseComment,
    Post,
    BaseCertificate,
    BaseRoll,
    RollPermission,
    HashtagRelation
)

from .serializers import (
    BaseSerializer,
    HashtagSerializer,
    HashtagParentSerializer,
    BaseCommentSerializer,
    PostSerializer,
    CertificateSerializer,
    RollSerializer,
    RollPermissionSerializer,
    HashtagRelationSerializer
)


class BaseModelViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        """class DynamicDeleteSerializer(ModelSerializer, BaseSerializer):
            class Meta:
                model = self.get_serializer_class().Meta.model
                fields = []

            def validate(self, attrs):
                if self.instance.delete_flag:
                    raise ValidationError('Ths selected object does not exist or already deleted.')
                return attrs"""

        try:
            instance = self.get_object()
            # serializer = DynamicDeleteSerializer(instance, request.data)
            # serializer.is_valid(raise_exception=True)
            instance.delete_flag = True
            instance.save()
            # return Response({status: "SUCCESS"}, status=status.HTTP_200_OK)
            response = HttpResponse(json.dumps({'message': 'record deleted.'}), content_type='application/json')
            response.status_code = 200
            return response
        except Exception as e:
            if type(e) is ValidationError:
                raise e

        return Response({
            "errors": [{
                "status": 1,
                "key": "non_field_errors",
                "detail": "The selected object does not exist or already deleted."
            }]
        })


class BaseViewset(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = Base.objects.all()
        child_name = self.request.query_params.get('child_name', None)
        if child_name is not None:
            queryset = queryset.filter(child_name=child_name)
        return queryset

    def get_serializer_class(self):
        return BaseSerializer


class HashtagParentViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = HashtagParent.objects.filter(delete_flag=False)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return HashtagParentSerializer

    
class HashtagViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsHashtagOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Hashtag.objects.filter(delete_flag=False)
        
        related_parent = self.request.query_params.get('related_parent', None)
        if related_parent is not None:
            queryset = queryset.filter(related_parent_id=related_parent)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return HashtagSerializer


class HashtagRelationViewset(BaseModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUserOrReadOnly]

    def get_queryset(self):
        queryset = HashtagRelation.objects.filter(delete_flag=False)

        hashtag_first = self.request.query_params.get('hashtag_first')
        if hashtag_first is not None:
            queryset = queryset.filter(hashtag_first=hashtag_first)

        hashtag_first_title = self.request.query_params.get('hashtag_first_title')
        if hashtag_first_title is not None:
            queryset = queryset.filter(hashtag_first__title=hashtag_first_title)

        hashtag_second = self.request.query_params.get('hashtag_second')
        if hashtag_second is not None:
            queryset = queryset.filter(hashtag_second=hashtag_second)

        hashtag_second_title = self.request.query_params.get('hashtag_second_title')
        if hashtag_second_title is not None:
            queryset = queryset.filter(hashtag_second__title=hashtag_second_title)

        active = self.request.query_params.get('active')
        if active is not None:
            queryset = queryset.filter(active=active)

        return queryset

    @list_route(methods=['get'], permission_classes=[IsAuthenticated])
    def search(self, request):
        relations = HashtagRelation.objects.filter(delete_flag=False)

        hashtag_text = self.request.query_params.get('hashtag_text')
        if hashtag_text is not None:
            try:
                hashtag_id = HashtagParent.objects.get(title=hashtag_text).id
            except HashtagParent.DoesNotExist:
                return []
            relations = relations.filter(Q(hashtag_first_id=hashtag_id) | Q(hashtag_second_id=hashtag_id))
            results = []
            for relation in relations:
                if relation.hashtag_first.id != hashtag_id:
                    results.append(relation.hashtag_first)
                else:
                    results.append(relation.hashtag_second)
            results_sorted = sorted(results, key=lambda x: x.usage, reverse=True)
        return Response(serializers.serialize('json', results_sorted), status=status.HTTP_200_OK)

    def get_serializer_class(self):
        return HashtagRelationSerializer


class BaseCommentViewset(BaseModelViewSet):
    parent_field = 'comment_parent'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = BaseComment.objects.filter(delete_flag=False)

        comment_parent = self.request.query_params.get('comment_parent', None)
        if comment_parent is not None:
            queryset = queryset.filter(comment_parent_id=comment_parent)

        comment_sender = self.request.query_params.get('comment_sender', None)
        if comment_sender is not None:
            queryset = queryset.filter(comment_sender_id=comment_sender)
        
        text = self.request.query_params.get('text', None)
        if text is not None:
            queryset = queryset.filter(text=text)

        return queryset

    def get_serializer_class(self):
        return BaseCommentSerializer


class PostViewSet(BaseModelViewSet):
    parent_field = 'post_parent'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(delete_flag=False).order_by('-id')

        post_type = self.request.query_params.get('post_type', None)
        if post_type is not None:
            queryset = queryset.filter(post_type=post_type)

        post_identity_id = self.request.query_params.get('post_identity_id', None)
        if post_identity_id is not None:
            queryset = queryset.filter(post_identity_id=post_identity_id)

        post_identity_name = self.request.query_params.get('post_identity_name', None)
        if post_identity_name is not None:
            queryset = queryset.filter(post_identity__name__contains=post_identity_name)

        post_related_product = self.request.query_params.get('post_related_product')
        if post_related_product is not None:
            queryset = queryset.filter(post_related_product_id=post_related_product)

        post_related_product_is_null = self.request.query_params.get('post_related_product_is_null')
        if post_related_product_is_null is not None and post_related_product_is_null == '0':
            print('salam')
            queryset = queryset.filter(~Q(post_related_product_id=None))

        post_title = self.request.query_params.get('post_title', None)
        if post_title is not None:
            queryset = queryset.filter(post_title__contains=post_title)

        post_description = self.request.query_params.get('post_description', None)
        if post_description is not None:
            queryset = queryset.filter(post_description__contains=post_description)

        post_parent = self.request.query_params.get('post_parent', None)
        if post_parent is not None:
            queryset = queryset.filter(post_parent_id=post_parent)

        post_pinned = self.request.query_params.get('post_pinned', None)
        if post_pinned is not None:
            queryset = queryset.filter(post_pinned=post_pinned)

        return queryset

    def get_serializer_class(self):
        return PostSerializer


class CertificateViewSet(BaseModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = BaseCertificate.objects.filter(delete_flag=False)

        certificate_identity = self.request.query_params.get('certificate_identity', None)
        if certificate_identity is not None:
            queryset = queryset.filter(certificate_identity=certificate_identity)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    def get_serializer_class(self):
        return CertificateSerializer


class RollViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsRollOwnerOrReadOnly]

    def get_queryset(self):
        queryset = BaseRoll.objects.filter(delete_flag=False)

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name=name)

        roll_parent = self.request.query_params.get('roll_parent', None)
        if roll_parent is not None:
            queryset = queryset.filter(roll_parent=roll_parent)

        user_roll = self.request.query_params.get('user_roll', None)
        if user_roll is not None:
            queryset = queryset.filter(user_roll=user_roll)

        user_roll_username = self.request.query_params.get('user_roll_username', None)
        if user_roll_username is not None:
            queryset = queryset.filter(user_roll__username=user_roll_username)

        return queryset

    def get_serializer_class(self):
        return RollSerializer


class RollPermissionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsRollPermissionOwnerOrReadOnly]

    def get_queryset(self):
        queryset = RollPermission.objects.filter(delete_flag=False)

        roll_permission_related_roll = self.request.query_params.get('roll_permission_related_roll', None)
        if roll_permission_related_roll is not None:
            queryset = queryset.filter(roll_permission_related_roll=roll_permission_related_roll)

        roll_permission_related_roll_name = self.request.query_params.get('roll_permission_related_roll_name', None)
        if roll_permission_related_roll_name is not None:
            queryset = queryset.filter(roll_permission_related_roll__name=roll_permission_related_roll_name)

        permission = self.request.query_params.get('permission', None)
        if permission is not None:
            queryset = queryset.filter(permission=permission)

        return queryset

    def get_serializer_class(self):
        return RollPermissionSerializer
