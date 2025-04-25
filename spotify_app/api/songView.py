from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.song import Song
from ..serializers.songserializers import songSerializer
from rest_framework.permissions import AllowAny

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = songSerializer
    permission_classes = [AllowAny]