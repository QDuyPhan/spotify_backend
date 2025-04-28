from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..models.album import Album
from ..serializers.albumserializers import albumSerializer


class AlbumViewSet(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        albums = Album.objects.all()
        serializer = albumSerializer(albums, many=True)
        return Response(serializer.data)

class AlbumDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, album_id):
        album = get_object_or_404(Album.objects.prefetch_related('songs'), id=album_id)
        serializer = albumSerializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)