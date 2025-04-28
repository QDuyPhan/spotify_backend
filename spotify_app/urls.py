from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.albumView import AlbumViewSet
# from .api.songView import SongViewSet
# from .api.userView import UserViewSet
from .api.adminView import AdminCheckView
from .api.userView import UserViewSet

router = DefaultRouter()
# router.register(r'songs', SongViewSet)
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
