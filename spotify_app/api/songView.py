import cloudinary
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from spotify_app.models.album import Album
from spotify_app.serializers.songserializers import songSerializer
import traceback

from ..auth.authentication import ClerkJWTAuthentication
from ..auth.permission import IsAdminUser
from ..models.song import Song



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


def upload_to_cloudinary(file):
    try:
        result = cloudinary.uploader.upload(file, resource_type="auto")
        return result
    except Exception as e:
        raise Exception("Error uploading to Cloudinary: " + str(e))

class CreateSongView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        try:
            if 'audioFile' not in request.FILES or 'imageFile' not in request.FILES:
                return Response({"message": "Please upload all required files"}, status=status.HTTP_400_BAD_REQUEST)

            title = request.data.get('title')
            artist = request.data.get('artist')
            duration = request.data.get('duration')
            album_id = request.data.get('album_id')

            if not all([title, artist, duration]):
                return Response({"message": "Title, artist, and duration are required."}, status=status.HTTP_400_BAD_REQUEST)

            audio_file = request.FILES['audioFile']
            image_file = request.FILES['imageFile']

            audio_upload = upload_to_cloudinary(audio_file)
            image_upload = upload_to_cloudinary(image_file)

            if not audio_upload or not image_upload:
                return Response({"message": "Failed to upload files"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            audio_url = audio_upload.get('secure_url')
            image_url = image_upload.get('secure_url')

            if not audio_url or not image_url:
                return Response({"message": "Failed to retrieve uploaded file URLs"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            album = None
            if album_id:
                try:
                    album = Album.objects.get(id=album_id)
                except Album.DoesNotExist:
                    return Response({"error": "Album not found"}, status=status.HTTP_404_NOT_FOUND)

            song = Song.objects.create(
                title=title,
                artist=artist,
                duration=int(duration),
                audio_url=audio_url,
                image_url=image_url,
                album=album
            )

            serializer = songSerializer(song)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)