import os
from dotenv import load_dotenv
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_GET
from django.http import JsonResponse
# Load biến môi trường
load_dotenv()

class AdminCheckViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="check")
    def check_admin(self, request):
        admin_email = os.getenv("ADMIN_EMAIL")
        user_email = request.user.email

        is_admin = user_email == admin_email
        return Response({
            "email": user_email,
            "is_admin": is_admin
        })
        
    @require_GET
    def create_song(request):
    # Giả sử bạn có thể truy cập request.user từ middleware
        return JsonResponse({"message": "Song created by admin!"})    
