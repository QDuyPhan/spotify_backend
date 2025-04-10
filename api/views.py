from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import user

# Create your views here.
User = get_user_model()


class ClerkAuthCallback(APIView):
    def post(self, request):
        clerk_id = request.data.get('id')
        first_name = request.data.get('firstName')
        last_name = request.data.get('lastName')
        fullName = f"{first_name} {last_name}"
        imageUrl = request.data.get('imageUrl')

        # Tìm hoặc tạo user bằng clerk_id
        user_obj, created = user.objects.get_or_create(
            clerk_id=clerk_id,
            defaults={
                'fullName': fullName,
                'imageUrl': imageUrl
            }
        )

        # Nếu user đã tồn tại, cập nhật fullName & imageUrl (nếu bạn muốn cập nhật)
        if not created:
            user_obj.fullName = fullName
            user_obj.imageUrl = imageUrl
            user_obj.save()

        return Response({"message": "User synced"}, status=status.HTTP_200_OK)