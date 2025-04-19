from rest_framework.exceptions import AuthenticationFailed
from django.utils.decorators import decorator_from_middleware
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from django.utils.decorators import decorator_from_middleware

# Middleware bảo vệ route (check người dùng đã đăng nhập)
class ProtectRouteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise AuthenticationFailed("Unauthorized - you must be logged in")
        return self.get_response(request)
        
# Middleware kiểm tra quyền Admin
class RequireAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Unauthorized - you must be logged in")

        # Kiểm tra quyền admin
        if request.user.email != settings.ADMIN_EMAIL:
            raise PermissionDenied("Unauthorized - you must be an admin")
        return self.get_response(request)