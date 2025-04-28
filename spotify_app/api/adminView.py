import os
from dotenv import load_dotenv
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from rest_framework.views import APIView

from spotify_app.auth.authentication import ClerkJWTAuthentication
from spotify_app.auth.permission import IsAdminUser

# Load biến môi trường
load_dotenv()


class AdminCheckView(APIView):
    authentication_classes = [ClerkJWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Kiểm tra email từ user object
        user_email = getattr(request.user, "email", None)
        if not user_email:
            return Response({"error": "Email not found in user object"}, status=400)

        print(f"🧾 User email from request: {user_email}")

        # Kiểm tra quyền admin
        admin_email = os.getenv("ADMIN_EMAIL", "phanquangduytvt@gmail.com")
        is_admin = user_email == admin_email

        if not is_admin:
            print(f"⛔ Unauthorized access attempt by: {user_email}")
            return Response({"message": "Unauthorized - admin privileges required"}, status=403)

        print(f"✅ Admin access granted to: {user_email}")
        return Response({
            "email": user_email,
            "admin": is_admin,
        })
