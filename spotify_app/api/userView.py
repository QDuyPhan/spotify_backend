from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.user import User
from ..serializers.userserializers import userSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        # Lấy ID người dùng hiện tại từ request.user   
        current_user = self.request.user
        print(f"Current user object: {current_user}")
        print(f"Type of current_user: {type(current_user)}")
        if current_user.is_authenticated:
            print(f"Current Clerk ID: {getattr(current_user, 'clerk_id', 'No clerk_id')}")
            return User.objects.exclude(clerk_id=current_user.clerk_id)
        else:
            return User.objects.none()    