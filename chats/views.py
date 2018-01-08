from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Message
from .serializers import MessageSerializer

# Create your views here.
class MessageViewSet(ModelViewSet):
    """
        A ViewSet for Handle Message Views
    """
    # queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Message.objects.all()

        sender_id = self.request.query_params.get('sender_id', None)
        if sender_id is not None:
            queryset = queryset.filter(message_sender_id=sender_id)

        sender_username = self.request.query_params.get('sender_username', None)
        if sender_username is not None:
            queryset = queryset.filter(message_sender__identity_user__username__contains=sender_username)

        receiver_id = self.request.query_params.get('receiver_id', None)
        if receiver_id is not None:
            queryset = queryset.filter(message_receiver_id=receiver_id)

        receiver_username = self.request.query_params.get('receiver_username', None)
        if receiver_username is not None:
            queryset = queryset.filter(message_receiver__identity_user__username__contains=receiver_username)

        body = self.request.query_params.get('body', None)
        if body is not None:
            queryset = queryset.filter(body__contains=body)

        return queryset

    def get_serializer_class(self):
        return MessageSerializer