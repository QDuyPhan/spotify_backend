from django.shortcuts import render
# 
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ..models import User 
# Create your views here.

class ClerkAuthCallback(APIView):
    def post(self, request):
        print("Request Data:", request.data)
        clerk_id = request.data.get('id')
        first_name = request.data.get('firstName', '')
        last_name = request.data.get('lastName', '')
        image_url = request.data.get('imageUrl', '')

        if not clerk_id:
            return Response(
                {"error": "clerk_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        full_name = f"{first_name} {last_name or ''}".strip()

        try:
            user, created = User.objects.get_or_create(
                clerk_id=clerk_id,
                defaults={
                    'fullName': full_name,
                    'imageUrl': image_url
                }
            )

            if not created:
                user.fullName = full_name
                user.imageUrl = image_url
                user.save()

            response_data = {
                "message": "User synced successfully",
                "user_id": user.id
            }
            print("Response Data:", response_data)

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print("Exception occurred during user get_or_create or save:", str(e))
            return Response(
                {"error": "Internal server error", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
