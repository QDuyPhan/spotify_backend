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