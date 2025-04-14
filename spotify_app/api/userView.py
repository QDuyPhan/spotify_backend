from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.user import User
from ..serializers.userserializers import userSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer
    