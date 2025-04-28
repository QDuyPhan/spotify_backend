from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..auth.authentication import ClerkJWTAuthentication
from ..auth.permission import IsAdminUser
from ..models.song import Song
from ..serializers.songserializers import songSerializer

# class SongViewSet(viewsets.ModelViewSet):


# queryset = Song.objects.all()
serializer_class = songSerializer


class GetAllSongsView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        songs = Song.objects.all().order_by("-created_at")
        print("songs: ", songs)
        return Response(songSerializer(songs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_featured_songs(request):
    songs = Song.objects.order_by("?")[:6]
    return Response(songSerializer(songs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_made_for_you_songs(request):
    songs = Song.objects.order_by("?")[:4]
    return Response(songSerializer(songs, many=True).data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_trending_songs(request):
    songs = Song.objects.order_by("-plays")[:4]
    return Response(songSerializer(songs, many=True).data)
