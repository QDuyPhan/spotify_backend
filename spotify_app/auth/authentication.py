import datetime
import json
import jwt
import requests
from rest_framework import authentication, exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jwt.algorithms import RSAAlgorithm
from ..models.user import User
from rest_framework.exceptions import AuthenticationFailed

# CLERK_JWKS_URL =  "https://picked-pigeon-9.clerk.accounts.dev/.well-known/jwks.json"
CLERK_JWKS_URL = "https://lucky-goat-46.clerk.accounts.dev/.well-known/jwks.json"

class ClerkJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            # Lấy public key từ Clerk
            jwks = requests.get(CLERK_JWKS_URL).json()
            unverified_header = jwt.get_unverified_header(token)
            public_key = None
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    public_key = RSAAlgorithm.from_jwk(key)
                    break

            if not public_key:
                print("❌ Không tìm thấy public key")
                raise AuthenticationFailed("Không tìm thấy public key")

            # Giải mã token
            payload = jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                # audience="pk_test_bHVja3ktZ29hdC00Ni5jbGVyay5hY2NvdW50cy5kZXYk",
                issuer="https://lucky-goat-46.clerk.accounts.dev",
                options={"verify_iat": False, "verify_nbf": False,"verify_aud": False}
            )
              # Tạo user object từ payload
            user_dict = {
                "email": payload.get("email_address"),
                "first_name": payload.get("first_name"),
                "last_name": payload.get("last_name"),
                "image_url": payload.get("imageUrl"),
                "is_authenticated": True,
                "is_active": True
            }
            
            # Đặc biệt quan trọng: Gán email vào cả attribute và property
            user = type("User", (), user_dict)
            user.email = payload.get("email_address")  # Thêm dòng này
            
            return (user, None)  # Trả về tuple (user, None)
        except Exception as e:
            print("❌ Lỗi xác thực:", str(e))
            raise AuthenticationFailed(f"Token không hợp lệ: {str(e)}")