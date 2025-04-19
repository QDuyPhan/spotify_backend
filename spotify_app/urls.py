from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.albumView import AlbumViewSet
from .api.songView import SongViewSet
from .api.userView import UserViewSet
from .api.adminView import AdminCheckViewSet
router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'albums', AlbumViewSet)
router.register(r'users', UserViewSet)
router.register(r'admin',AdminCheckViewSet, basename='admin')
urlpatterns = [
    path('', include(router.urls)),
]