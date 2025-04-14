from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.song import Song
from ..serializers.songserializers import songSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = songSerializer
    