from rest_framework.serializers import ModelSerializer

from .models import Message

# define serializers here
class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('send_date', 'seen_date')