import datetime
import json
import jwt
import requests
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt import algorithms
from ..models.user import User

CLERK_JWKS_URL = "https://picked-pigeon-9.clerk.accounts.dev/.well-known/jwks.json"


class ClerkJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            jwks = requests.get(CLERK_JWKS_URL).json()
            unverified_header = jwt.get_unverified_header(token)
            public_key = None
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    public_key = algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
                    break

            if not public_key:
                print("❌ Không tìm thấy public key")
                raise AuthenticationFailed("Không tìm thấy public key")

            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                issuer="https://picked-pigeon-9.clerk.accounts.dev",
                options={"verify_iat": False, "verify_nbf": False, "verify_aud": False}
            )

            user_dict = {
                "email": payload.get("email_address"),
                "first_name": payload.get("first_name"),
                "last_name": payload.get("last_name"),
                "image_url": payload.get("imageUrl"),
                "clerk_id": payload.get("sub"),
                "is_authenticated": True,
                "is_active": True
            }

            user = type("User", (), user_dict)
            user.email = payload.get("email_address")

            return (user, None)
        except Exception as e:
            print("❌ Lỗi xác thực:", str(e))
            raise AuthenticationFailed(f"Token không hợp lệ: {str(e)}")
