from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny


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


class BaseViewset(ModelViewSet):
    # queryset = Base.objects.all()
    permission_classes = ""

    def get_queryset(self):
        return Base.objects.all()

    def get_serializer_class(self):
        return BaseSerializer


class HashtagParentViewset(ModelViewSet):
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

    
class HashtagViewset(ModelViewSet):
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


class BaseCommentViewset(ModelViewSet):
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


class PostViewSet(ModelViewSet):
    # queryset = Post.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Post.objects.all()

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


class CertificateViewSet(ModelViewSet):
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