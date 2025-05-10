import traceback
import cloudinary
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import os

from spotify_app.models.user import User
from ..models.song import Song

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
        print("album ${album}")
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
        
class DeleteAlbumView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        print(f"Attempting to delete album with ID: {id}")
        try:
            # Lấy thông tin user từ JWT
            clerk_id = getattr(request.user, "clerk_id", None)
            print(f"User clerk_id: {clerk_id}")
            if not clerk_id:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                user = User.objects.get(clerk_id=clerk_id)
                print(f"Found user: {user.id}")
            except User.DoesNotExist:
                print("User not found in database")
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Kiểm tra quyền admin dựa vào email
            user_email = getattr(request.user, "email", None)
            admin_email = os.getenv("ADMIN_EMAIL", "phanquangduytvt@gmail.com")
            is_admin = user_email == admin_email
            print(f"User email: {user_email}, is_admin: {is_admin}")
            if not is_admin:
                # Nếu không phải admin, chỉ cho phép xóa album của mình
                try:
                    album = Album.objects.get(pk=id, owner=user)
                    print(f"Found album: {album.id} - {album.title}")
                except Album.DoesNotExist:
                    print(f"Album {id} not found or not owned by user {user.id}")
                    return Response({"error": "Album not found or you do not have permission to delete it"}, 
                                  status=status.HTTP_404_NOT_FOUND)
            else:
                # Nếu là admin, cho phép xóa bất kỳ album nào
                try:
                    album = Album.objects.get(pk=id)
                    print(f"[ADMIN] Found album: {album.id} - {album.title}")
                except Album.DoesNotExist:
                    print(f"[ADMIN] Album {id} not found")
                    return Response({"error": "Album not found"}, status=status.HTTP_404_NOT_FOUND)

            # Xóa hình ảnh trên Cloudinary nếu có
            if album.image_url:
                try:
                    public_id = album.image_url.split('/')[-1].split('.')[0]
                    print(f"Deleting image from Cloudinary: {public_id}")
                    cloudinary.uploader.destroy(public_id)
                except Exception as e:
                    print(f"Error deleting image from Cloudinary: {str(e)}")

            # Lấy danh sách bài hát trong album
            songs = album.songs.all()
            print(f"Found {songs.count()} songs in album")
            
            # Xóa các file nhạc trên Cloudinary
            for song in songs:
                if song.audio_url:
                    try:
                        public_id = song.audio_url.split('/')[-1].split('.')[0]
                        print(f"Deleting audio from Cloudinary: {public_id}")
                        cloudinary.uploader.destroy(public_id)
                    except Exception as e:
                        print(f"Error deleting audio from Cloudinary: {str(e)}")

            # Xóa các bản ghi trong bảng AlbumSong
            from spotify_app.models.albumSong import AlbumSong
            print("Deleting AlbumSong records")
            AlbumSong.objects.filter(album=album).delete()

            # Xóa album
            print("Deleting album")
            album.delete()

            return Response({
                "message": "Album and associated songs deleted successfully",
                "deleted_album_id": id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error in DeleteAlbumView: {str(e)}")
            traceback.print_exc()
            return Response({
                "error": "An error occurred while deleting the album",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CreateAlbumByUserView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            title = request.data.get('title')
            artist = request.data.get('artist')
            release_year = request.data.get('release_year')
            image_file = request.FILES.get('imageFile')

            if not all([title, artist, release_year, image_file]):
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

            image_url = upload_to_cloudinary(image_file)

            # ✅ Lấy User thật từ DB bằng clerk_id từ JWT payload
            clerk_id = getattr(request.user, "clerk_id", None)
            if not clerk_id:
                return Response({"error": "User authentication failed"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                user = User.objects.get(clerk_id=clerk_id)
            except User.DoesNotExist:
                return Response({"error": "User not found in database"}, status=status.HTTP_404_NOT_FOUND)

            album = Album.objects.create(
                title=title,
                artist=artist,
                image_url=image_url,
                release_year=release_year,
                owner=user
            )

            serializer = albumSerializer(album)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ListAlbumsOfUserView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            clerk_id = getattr(request.user, "clerk_id", None)
            if not clerk_id:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                user = User.objects.get(clerk_id=clerk_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            albums = Album.objects.filter(owner=user).order_by("-id")
            serializer = albumSerializer(albums, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumSongsOfUserView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, album_id):
        try:
            clerk_id = getattr(request.user, "clerk_id", None)
            if not clerk_id:
                return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                user = User.objects.get(clerk_id=clerk_id)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                album = Album.objects.get(id=album_id, owner=user)
            except Album.DoesNotExist:
                return Response({"error": "Album not found or you do not have permission."}, status=status.HTTP_404_NOT_FOUND)

            songs = album.songs.all()
            from spotify_app.serializers.songserializers import songSerializer
            serializer = songSerializer(songs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)