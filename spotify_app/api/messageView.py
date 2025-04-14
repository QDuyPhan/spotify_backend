from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.message import Message
from ..serializers.messageserializers import messageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = messageSerializer
    