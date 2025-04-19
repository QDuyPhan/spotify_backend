from django.http import JsonResponse
from django.conf import settings
import jwt
import requests
from django.core.cache import cache
from spotify_app.models import CustomUser

class ProtectRouteMiddleware:


    def __call__(self, request):
        # Bỏ qua các URL công khai
        public_paths = ['/auth/callback/', '/login/', '/signup/']
        if request.path in public_paths:
            return self.get_response(request)

        # Kiểm tra header Authorization
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return JsonResponse(
                {'message': 'Unauthorized - you must be logged in'},
                status=401
            )

        # Xác minh JWT
        token = auth_header.split(' ')[1]
        try:
            # Cache JWKS
            cache_key = 'clerk_jwks'
            jwks = cache.get(cache_key)
            if not jwks:
                response = requests.get(settings.CLERK_JWKS_URL)
                if response.status_code != 200:
                    raise Exception("Failed to fetch JWKS")
                jwks = response.json()
                cache.set(cache_key, jwks, timeout=3600)

            # Lấy public key
            unverified_header = jwt.get_unverified_header(token)
            public_key = None
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                    break
            if not public_key:
                raise Exception("Public key not found")

            # Decode JWT
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=settings.CLERK_AUDIENCE
            )

            # Lấy user từ CustomUser
            user_id = payload["sub"]
            email = payload.get("email_address")  # Lấy email từ JWT, không lưu
            try:
                user = CustomUser.objects.get(clerk_id=user_id)
            except CustomUser.DoesNotExist:
                return JsonResponse(
                    {'message': 'Unauthorized - user not found'},
                    status=401
                )

            # Gắn thông tin vào request
            request.auth = {'userId': user_id, 'email': email}
            request.user = user
            request.user.is_admin = email == settings.ADMIN_EMAIL
        except Exception as e:
            return JsonResponse(
                {'message': 'Unauthorized - invalid token', 'error': str(e)},
                status=401
            )

        return self.get_response(request)