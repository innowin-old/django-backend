from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from .models import (
        Organization,
        StaffCount,
        Picture
    )

from .serializers import (
        OrganizationSerializer,
        StaffCountSerializer,
        PictureSerializer
    )


class OrganizationViewset(ModelViewSet):
    queryset = Organization.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return OrganizationSerializer


class StaffCountViewset(ModelViewSet):
    queryset = StaffCount.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return StaffCountSerializer


class PictureViewset(ModelViewSet):
    queryset = Picture.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return PictureSerializer
