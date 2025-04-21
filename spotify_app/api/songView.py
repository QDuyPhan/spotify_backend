from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.song import Song
from ..serializers.songserializers import songSerializer

# class SongViewSet(viewsets.ModelViewSet):


# queryset = Song.objects.all()
serializer_class = songSerializer


@api_view(['GET'])
def get_all_songs(request):
    songs = Song.objects.all().order_by("-created_at")
    return Response(songSerializer(songs, many=True).data)


@api_view(['GET'])
def get_featured_songs(request):
    songs = Song.objects.order_by("?")[:6]
    return Response(songSerializer(songs, many=True).data)


@api_view(['GET'])
def get_made_for_you_songs(request):
    songs = Song.objects.order_by("?")[:4]
    return Response(songSerializer(songs, many=True).data)


@api_view(['GET'])
def get_trending_songs(request):
    songs = Song.objects.order_by("-plays")[:4]
    return Response(songSerializer(songs, many=True).data)
