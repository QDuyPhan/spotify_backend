from django.core.cache import cache
from django.http import JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from spotify_app.auth.authentication import ClerkJWTAuthentication
from spotify_app.auth.permission import IsAdminUser
from spotify_app.models import Song, Album, User

class StatsView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, *args, **kwargs):
        try:
            total_songs = Song.objects.count()
            total_albums = Album.objects.count()
            total_users = User.objects.count()

            song_artists = Song.objects.values_list('artist', flat=True)
            album_artists = Album.objects.values_list('artist', flat=True)

            all_artists = list(song_artists) + list(album_artists)
            unique_artists_count = len(set(all_artists))

            return JsonResponse({
                "totalAlbums": total_albums,
                "totalSongs": total_songs,
                "totalUsers": total_users,
                "totalArtists": unique_artists_count
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)