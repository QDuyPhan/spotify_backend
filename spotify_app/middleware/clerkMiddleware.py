import jwt
import requests
from rest_framework import authentication, exceptions

CLERK_JWKS_URL =  "https://picked-pigeon-9.clerk.accounts.dev/.well-known/jwks.json"
#CLERK_JWKS_URL =  "https://novel-fish-82.clerk.accounts.dev/.well-known/jwks.json"
class ClerkJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        token = auth_header.split(" ")[1]

        try:
            jwks = requests.get(CLERK_JWKS_URL).json()
            public_key = self.get_public_key(jwks, token)
            payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="pk_test_cGlja2VkLXBpZ2Vvbi05LmNsZXJrLmFjY291bnRzLmRldiQ")
            
            #payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="pk_test_bm92ZWwtZmlzaC04Mi5jbGVyay5hY2NvdW50cy5kZXYk")
        except Exception as e:
            raise exceptions.AuthenticationFailed("Invalid Clerk token")

        user = type("User", (), {"id": payload["sub"], "email": payload.get("email_address")})()
        return (user, None)

    def get_public_key(self, jwks, token):
        unverified_header = jwt.get_unverified_header(token)
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                return jwt.algorithms.RSAAlgorithm.from_jwk(key)
        raise Exception("Public key not found")

# import os
# import jwt
# import requests
# from rest_framework import authentication, exceptions

# ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")  # đặt email admin trong biến môi trường

# class ClerkJWTAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.headers.get("Authorization")
#         if not auth_header:
#             return None

#         token = auth_header.split(" ")[1]

#         try:
#             jwks = requests.get("https://picked-pigeon-9.clerk.accounts.dev/.well-known/jwks.json").json()
#             public_key = self.get_public_key(jwks, token)
#             payload = jwt.decode(token, public_key, algorithms=["RS256"], audience="pk_test_cGlja2VkLXBpZ2Vvbi05LmNsZXJrLmFjY291bnRzLmRldiQ")
#         except Exception:
#             raise exceptions.AuthenticationFailed("Invalid Clerk token")

#         # Tạo user giả (hoặc custom User object nếu cần)
#         user = type("User", (), {
#             "id": payload["sub"],
#             "email": payload.get("email_address"),
#             "is_admin": payload.get("email_address") == ADMIN_EMAIL
#         })()

#         return (user, None)
    
#     def get_public_key(self, jwks, token):
#         unverified_header = jwt.get_unverified_header(token)
#         for key in jwks["keys"]:
#             if key["kid"] == unverified_header["kid"]:
#                 return jwt.algorithms.RSAAlgorithm.from_jwk(key)
#         raise Exception("Public key not found")

# from django.http import JsonResponse
# from django.conf import settings
# import jwt
# import requests
# from django.core.cache import cache
# from spotify_app.models.user import User 

# class ProtectRouteMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Bỏ qua các URL công khai
#         public_paths = ['/auth/callback/', '/login/', '/signup/']
#         if request.path in public_paths:
#             return self.get_response(request)

#         # Kiểm tra header Authorization
#         auth_header = request.headers.get('Authorization', '')
#         if not auth_header.startswith('Bearer '):
#             return JsonResponse(
#                 {'message': 'Unauthorized - you must be logged in'},
#                 status=401
#             )

#         # Xác minh JWT (logic từ ClerkJWTAuthentication)
#         token = auth_header.split(' ')[1]
#         try:
#             # Cache JWKS
#             cache_key = "https://picked-pigeon-9.clerk.accounts.dev/.well-known/jwks.json"
#             jwks = cache.get(cache_key)
#             if not jwks:
#                 response = requests.get(settings.CLERK_JWKS_URL)
#                 if response.status_code != 200:
#                     raise Exception("Failed to fetch JWKS")
#                 jwks = response.json()
#                 cache.set(cache_key, jwks, timeout=3600)

#             # Lấy public key
#             unverified_header = jwt.get_unverified_header(token)
#             public_key = None
#             for key in jwks["keys"]:
#                 if key["kid"] == unverified_header["kid"]:
#                     public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
#                     break
#             if not public_key:
#                 raise Exception("Public key not found")

#             # Decode JWT
#             payload = jwt.decode(
#                 token,
#                 public_key,
#                 algorithms=["RS256"],
#                 audience="pk_test_cGlja2VkLXBpZ2Vvbi05LmNsZXJrLmFjY291bnRzLmRldiQ"
#             )

#             # Lấy user từ CustomUser
#             user_id = payload["sub"]
#             email = payload.get("email_address")
#             try:
#                 user = User.objects.get(clerk_id=user_id)
#             except User.DoesNotExist:
#                 return JsonResponse(
#                     {'message': 'Unauthorized - user not found'},
#                     status=401
#                 )

#             # Gắn thông tin vào request
#             request.auth = {'userId': user_id, 'email': email}
#             request.user = user
#             request.user.is_admin = email == settings.ADMIN_EMAIL
#         except Exception as e:
#             return JsonResponse(
#                 {'message': 'Unauthorized - invalid token', 'error': str(e)},
#                 status=401
#             )

#         return self.get_response(request)

# class RequireAdminMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Chỉ áp dụng cho tuyến đường /admin/
#         if not request.path.startswith('/admin/'):
#             return self.get_response(request)

#         # Kiểm tra đăng nhập
#         if not hasattr(request, 'user') or not request.user:
#             return JsonResponse(
#                 {'message': 'Unauthorized - you must be logged in'},
#                 status=401
#             )

#         # Kiểm tra quyền admin
#         try:
#             if not request.user.is_admin:
#                 return JsonResponse(
#                     {'message': 'Unauthorized - you must be an admin'},
#                     status=403
#                 )
#         except Exception as e:
#             return JsonResponse(
#                 {'message': 'Internal server error', 'error': str(e)},
#                 status=500
#             )

#         return self.get_response(request)