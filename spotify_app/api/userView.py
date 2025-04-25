from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.user import User
from ..serializers.userserializers import userSerializer
from rest_framework.permissions import AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userSerializer
    permission_classes = [AllowAny]
    # def get_queryset(self):
        # Lấy ID người dùng hiện tại từ request.user
        # current_user = self.request.user
        # if current_user.is_authenticated:
            # Loại bỏ người dùng hiện tại khỏi queryset
            # return User.objects.exclude(id=current_user.id)
        # User.objects.exclude(id=current_user.id)
        # else:
            # Nếu không có người dùng đăng nhập, trả về queryset rỗng hoặc xử lý theo yêu cầu
            # return User.objects.none()    