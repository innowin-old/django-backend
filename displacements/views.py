from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from products.models import Product
from .serializers import GetUserDataSerializer, GetProductDataSerializer


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