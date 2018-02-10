from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from .serializers import BaseSerializer

import json

from .models import (
    Base,
    Hashtag,
    HashtagParent,
    BaseComment,
    Post,
    BaseCertificate
)

from .serializers import (
    BaseSerializer,
    HashtagSerializer,
    HashtagParentSerializer,
    BaseCommentSerializer,
    PostSerializer,
    CertificateSerializer
)


class BaseModelViewSet(ModelViewSet):
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
            #return Response({status: "SUCCESS"}, status=status.HTTP_200_OK)
            response = HttpResponse(json.dumps({'message': 'record deleted.'}), 
                content_type='application/json')
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
    # queryset = Base.objects.all()
    permission_classes = ""

    def get_queryset(self):
        return Base.objects.all()

    def get_serializer_class(self):
        return BaseSerializer


class HashtagParentViewset(BaseModelViewSet):
    # queryset = HashtagParent.objects.all()
    permisison_classes = ""

    def get_queryset(self):
        queryset = HashtagParent.objects.all()

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return HashtagParentSerializer

    
class HashtagViewset(BaseModelViewSet):
    # queryset = Hashtag.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Hashtag.objects.all()
        
        related_parent = self.request.query_params.get('related_parent', None)
        if related_parent is not None:
            queryset = queryset.filter(related_parent_id=related_parent)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return HashtagSerializer


class BaseCommentViewset(BaseModelViewSet):
    # queryset = BaseComment.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = BaseComment.objects.all()

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
    # queryset = Post.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Post.objects.filter(delete_flag=False)

        post_type = self.request.query_params.get('post_type', None)
        if post_type is not None:
            queryset = queryset.filter(post_type=post_type)

        post_identity_id = self.request.query_params.get('post_identity_id', None)
        if post_identity_id is not None:
            queryset = queryset.filter(post_identity_id=post_identity_id)

        post_identity_name = self.request.query_params.get('post_identity_name', None)
        if post_identity_name is not None:
            queryset = queryset.filter(post_identity__name__contains=post_identity_name)

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
    #queryset = BaseCertificate.objects.all()

    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = BaseCertificate.objects.all()

        certificate_identity = self.request.query_params.get('certificate_identity', None)
        if certificate_identity is not None:
            queryset = queryset.filter(certificate_identity=certificate_identity)

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title__contains=title)

        return queryset

    def get_serializer_class(self):
        return CertificateSerializer
