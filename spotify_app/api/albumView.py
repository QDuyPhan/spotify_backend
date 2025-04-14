from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.album import Album
from ..serializers.albumserializers import albumSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = albumSerializer
    