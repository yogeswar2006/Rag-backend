from rest_framework.serializers import ModelSerializer
from .models import ChatRoom

class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model=ChatRoom
        fields = ['id','title','created_at']