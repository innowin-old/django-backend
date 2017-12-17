from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import detail_route, list_route

from .models import Message
from .serializers import MessageSerializer

# Create your views here.
class MessageViewSet(ModelViewSet):
    """
        A ViewSet for Handle Message Views
    """
    queryset = Message.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return MessageSerializer