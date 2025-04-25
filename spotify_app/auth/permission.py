# spotify_app/permissions.py
from rest_framework import permissions
import os

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user_email = getattr(request.user, "email", None)
        if not user_email:
            return False
        
        admin_email = os.getenv("ADMIN_EMAIL", "minhthinh9229@gmail.com")
        return user_email == admin_email