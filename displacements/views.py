from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from exchanges.models import Exchange
from products.models import Product
from organizations.models import Organization
from .serializers import GetUserDataSerializer, GetProductDataSerializer, GetOrganizationDataSerializer, GetExchangeDataSerializer


# Create your views here.
class GetUserDataViewset(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        return GetUserDataSerializer


class GetProductDataViewset(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset

    def get_serializer_class(self):
        return GetProductDataSerializer


class GetOrganizationDataViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Organization.objects.all()
        return queryset

    def get_serializer_class(self):
        return GetOrganizationDataSerializer


class GetExchangeDataViwSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Exchange.objects.all()
        return queryset

    def get_serializer_class(self):
        return GetExchangeDataSerializer