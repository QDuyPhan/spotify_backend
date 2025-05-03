from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from ..models.message import Message
from ..serializers.messageserializers import messageSerializer
from ..serializers.userserializers import userSerializer

# Lấy model User từ settings.AUTH_USER_MODEL
User = get_user_model()

@api_view(['GET'])
def get_messages_by_clerk_id(request, clerk_id):
    print("🔍 Nhận yêu cầu lấy tin nhắn với clerk_id:", clerk_id)

    # Kiểm tra clerk_id không hợp lệ
    if not clerk_id or clerk_id == "undefined":
        print("❌ clerk_id không hợp lệ:", clerk_id)
        return Response({"detail": "Invalid clerk_id"}, status=400)

    # Lấy clerk_id của người gửi từ request.user
    sender_clerk_id = getattr(request.user, "clerk_id", None)
    if not sender_clerk_id:
        print("❌ Không tìm thấy clerk_id của người gửi trong request.user")
        return Response({"detail": "Unauthorized"}, status=401)

    try:
        # Kiểm tra người gửi
        sender = User.objects.get(clerk_id=sender_clerk_id)
        print("✅ Người gửi:", sender)
    except User.DoesNotExist:
        print(f"❌ Người gửi với clerk_id {sender_clerk_id} không tồn tại trong database")
        return Response({"detail": "Sender not found"}, status=404)
    except Exception as e:
        print(f"❌ Lỗi khi tìm người gửi: {str(e)}")
        return Response({"detail": "Error fetching sender"}, status=500)

    try:
        # Kiểm tra người nhận
        receiver = User.objects.get(clerk_id=clerk_id)
        print("✅ Người nhận:", receiver)
    except User.DoesNotExist:
        print(f"❌ Người nhận với clerk_id {clerk_id} không tồn tại trong database")
        return Response({"detail": "Receiver not found"}, status=404)
    except Exception as e:
        print(f"❌ Lỗi khi tìm người nhận: {str(e)}")
        return Response({"detail": "Error fetching receiver"}, status=500)

    try:
        # Tìm tin nhắn giữa sender và receiver
        messages = Message.objects.filter(
            sender=sender, receiver=receiver
        ) | Message.objects.filter(
            sender=receiver, receiver=sender
        )
        messages = messages.order_by("created_at")

        print(f"✅ Tìm thấy {messages.count()} tin nhắn giữa {sender_clerk_id} và {clerk_id}")

        serializer = messageSerializer(messages, many=True)
        return Response(serializer.data, status=200)

    except Exception as e:
        print("❌ Lỗi khi lấy tin nhắn:", str(e))
        return Response({"detail": f"Error fetching messages: {str(e)}"}, status=500)