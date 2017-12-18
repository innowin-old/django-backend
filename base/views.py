from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny


from .models import (
    Hashtag,
    HashtagParent
)

from .serializers import (
    HashtagSerializer,
    HashtagParentSerializer
)


class HashtagParentViewset(ModelViewSet):
    queryset = HashtagParent.objects.all()
    permisison_classes = ""

    def get_queryset(self):
        queryset = HashtagParent.objects.all()

        related_parent = self.request.query_params.get('related_parent', None)
        if related_parent is not None:
            queryset = queryset.filter(related_parent_id=related_parent)

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

        c_type = self.request.query_params.get('c_type', None)
        if c_type is not None:
            queryset = queryset.filter(c_type=c_type)

        related_instance = self.request.query_params.get('related_instance', None)
        if related_instance is not None:
            queryset = queryset.filter(related_instance_id=related_instance)

        return queryset

    def get_serializer_class(self):
        return HashtagSerializer
