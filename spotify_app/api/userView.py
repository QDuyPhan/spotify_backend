from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from ..models.user import User
from ..serializers.userserializers import userSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Lấy ID người dùng hiện tại từ request.user

        current_user = self.request.user
        print(f"Current user object: {current_user}")
        print(f"Type of current_user: {type(current_user)}")
        if current_user.is_authenticated:
            # Loại bỏ người dùng hiện tại khỏi queryset
            # return User.objects.exclude(id=current_user.id)
            # print(f"Current user ID: {current_user.id}")  # <-- thêm dòng này
            # return User.objects.exclude(id=getattr(current_user, 'id', None))
            print(f"Current Clerk ID: {getattr(current_user, 'clerk_id', 'No clerk_id')}")
            return User.objects.exclude(clerk_id=current_user.clerk_id)
        else:
            # User.objects.exclude(id=current_user.id)
            # Nếu không có người dùng đăng nhập, trả về queryset rỗng hoặc xử lý theo yêu cầu
            return User.objects.none()
