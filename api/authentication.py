import jwt
import requests
from .models import user
from rest_framework import authentication, exceptions
from django.conf import settings

class ClerkJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            jwks = requests.get(settings.CLERK_JWKS_URL).json()
            public_key = self.get_public_key(jwks, token)
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=settings.CLERK_AUDIENCE
            )
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Invalid Clerk token: {str(e)}")

        clerk_id = payload["sub"]
        full_name = f"{payload.get('first_name', '')} {payload.get('last_name', '')}".strip()
        image_url = payload.get("image_url", "")
        email = payload.get("email")

        user_obj, _ = user.objects.get_or_create(
            clerk_id=clerk_id,
            defaults={
                "fullName": full_name,
                "imageUrl": image_url,
                "email": email
            }
        )

        # Optional: Update fields if user exists
        user_obj.fullName = full_name
        user_obj.imageUrl = image_url
        user_obj.email = email
        user_obj.save()

        return (user_obj, None)

    def get_public_key(self, jwks, token):
        unverified_header = jwt.get_unverified_header(token)
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                return jwt.algorithms.RSAAlgorithm.from_jwk(key)
        raise Exception("Public key not found")