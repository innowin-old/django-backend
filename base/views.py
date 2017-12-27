from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny


from .models import (
    Base,
    Hashtag,
    HashtagParent,
    BaseComment
)

from .serializers import (
    BaseSerializer,
    HashtagSerializer,
    HashtagParentSerializer,
    BaseCommentSerializer
)


class BaseViewset(ModelViewSet):
    # queryset = Base.objects.all()
    permission_classes = ""

    def get_queryset(self):
        return Base.objects.all()

    def get_serializer_class(self):
        return BaseSerializer


class HashtagParentViewset(ModelViewSet):
    queryset = HashtagParent.objects.all()
    permisison_classes = ""

    def get_queryset(self):
        queryset = HashtagParent.objects.all()

        title = self.request.query_params.get('title', None)
        if title is not None:
            queryset = queryset.filter(title=title)

        return queryset

    def get_serializer_class(self):
        return HashtagParentSerializer

    
class HashtagViewset(ModelViewSet):
    queryset = Hashtag.objects.all()
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


class BaseCommentViewset(ModelViewSet):
    queryset = BaseComment.objects.all()
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
