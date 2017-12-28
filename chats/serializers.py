from base.serializers import BaseSerializer

from .models import Message

# define serializers here
class MessageSerializer(BaseSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('send_date', 'seen_date')