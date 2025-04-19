from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import user
from api.models.album import Album
from rest_framework.decorators import api_view
from api.serializer import albumSerializer
from api.serializer import userSerializer
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import PermissionDenied
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from .authentication import ClerkJWTAuthentication
# Create your views here.
User = get_user_model()

class ClerkAuthCallback(APIView):
    def post(self, request):
        clerk_id = request.data.get('id')
        first_name = request.data.get('firstName', '')
        last_name = request.data.get('lastName', '')
        full_name = f"{first_name} {last_name}".strip()
        image_url = request.data.get('imageUrl', '')
        email = request.data.get('email', '')

        user_obj, created = user.objects.get_or_create(
            clerk_id=clerk_id,
            defaults={
                'fullName': full_name,
                'imageUrl': image_url,
                'email': email,
            }
        )

        # Optional update if user already exists
        if not created:
            user_obj.fullName = full_name
            user_obj.imageUrl = image_url
            user_obj.email = email
            user_obj.save()

        return Response({"message": "User synced"}, status=status.HTTP_200_OK)
    

class CheckAdminView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.email != settings.ADMIN_EMAIL:
            raise PermissionDenied("Unauthorized - you must be an admin")
        return Response({"admin": True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    current_user_clerk_id = request.user.clerk_id
    users = user.objects.exclude(clerk_id=current_user_clerk_id)
    serializer = userSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_all_albums(request):
    albums = Album.objects.all()
    serializer = albumSerializer(albums, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_album_by_id(request, id):
    try:
        album = Album.objects.prefetch_related('songs').get(id=id)
        serializer = albumSerializer(album)
        return Response(serializer.data)
    except Album.DoesNotExist:
        return Response({'message': 'Album not found'}, status=status.HTTP_404_NOT_FOUND)