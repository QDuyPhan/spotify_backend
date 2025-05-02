import cloudinary
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from spotify_app.models.album import Album
from spotify_app.models.user import User
from spotify_app.serializers.songserializers import songSerializer
import traceback
from django.contrib.auth import get_user_model

from ..auth.authentication import ClerkJWTAuthentication
from ..auth.permission import IsAdminUser
from ..models.song import Song



# queryset = Song.objects.all()
serializer_class = songSerializer

class GetAllSongsView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

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
        
        
class DeleteSongView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, id):
        try:
            song = Song.objects.get(pk=id)

            if song.album_id:
                album = Album.objects.get(pk=song.album_id)
                if hasattr(album, "songs"):
                    album.songs.remove(song)

            song.delete()

            return Response({"message": "Song deleted successfully"}, status=status.HTTP_200_OK)

        except Song.DoesNotExist:
            return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("Error in DeleteSongView:", e)
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddSongToAlbumView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get data from request
            album_id = request.data.get('album_id')
            song_id = request.data.get('song_id')

            # Validate required fields
            if not album_id or not song_id:
                missing_fields = []
                if not album_id:
                    missing_fields.append("album_id")
                if not song_id:
                    missing_fields.append("song_id")
                return Response(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get clerk_id from request.user
            clerk_id = getattr(request.user, 'clerk_id', None)
            if not clerk_id:
                return Response(
                    {"error": "Clerk ID not found in token."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Find user by clerk_id
            try:
                real_user = User.objects.get(clerk_id=clerk_id)
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Find album and check ownership
            try:
                album = Album.objects.get(id=album_id, owner=real_user)
            except Album.DoesNotExist:
                return Response(
                    {"error": "Album not found or does not belong to the user."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Find song
            try:
                song = Song.objects.get(id=song_id)
            except Song.DoesNotExist:
                return Response(
                    {"error": "Song not found."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if song already exists in album
            if album.songs.filter(id=song.id).exists():
                return Response(
                    {"error": "Song already exists in this album."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Add song to album using many-to-many relationship
            album.songs.add(song)

            # Return success response with song data
            serializer = songSerializer(song)
            return Response({
                "message": "Song added to album successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FavoriteSongView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        song_id = request.data.get('song_id')
        if not song_id:
            return Response({"error": "Missing song_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(clerk_id=getattr(request.user, "clerk_id", None))
            song = Song.objects.get(id=song_id)
            user.favorite_songs.add(song)
            return Response({"message": "Added to favorites"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Song.DoesNotExist:
            return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        song_id = request.data.get('song_id')
        if not song_id:
            return Response({"error": "Missing song_id"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(clerk_id=getattr(request.user, "clerk_id", None))
            song = Song.objects.get(id=song_id)
            user.favorite_songs.remove(song)
            return Response({"message": "Removed from favorites"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Song.DoesNotExist:
            return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)

class ListFavoriteSongsView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(clerk_id=getattr(request.user, "clerk_id", None))
            songs = user.favorite_songs.all()
            serializer = songSerializer(songs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)