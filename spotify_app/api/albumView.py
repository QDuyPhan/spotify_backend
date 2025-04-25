from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.album import Album
from ..serializers.albumserializers import albumSerializer
from rest_framework.permissions import AllowAny


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = albumSerializer
    permission_classes = [AllowAny]