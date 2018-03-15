from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from .serializers import GetUserDataSerializer


# Create your views here.
class GetUserDataViewset(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

    def get_serializer_class(self):
        return GetUserDataSerializer
