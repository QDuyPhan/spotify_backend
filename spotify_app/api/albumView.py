import traceback
import cloudinary
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from spotify_app.auth.authentication import ClerkJWTAuthentication
from spotify_app.auth.permission import IsAdminUser

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
    
def upload_to_cloudinary(file):
    try:
        result = cloudinary.uploader.upload(file, resource_type="auto")
        return result.get('secure_url')
    except Exception as e:
        raise Exception("Error uploading to Cloudinary: " + str(e))
    
class CreateAlbumView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        try:
            title = request.data.get('title')
            artist = request.data.get('artist')
            release_year = request.data.get('release_year')
            image_file = request.FILES.get('imageFile')

            if not all([title, artist, release_year, image_file]):
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

            image_url = upload_to_cloudinary(image_file)

            album = Album.objects.create(
                title=title,
                artist=artist,
                image_url=image_url,
                release_year=release_year
            )

            serializer = albumSerializer(album)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)