"""
URL configuration for spotify_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from spotify_app.api.adminView import AdminCheckView
from spotify_app.api.albumView import AlbumViewSet, AlbumDetailAPIView, CreateAlbumView
from spotify_app.api.authenticationView import *
from spotify_app.api.songView import (
    CreateSongView,
    get_featured_songs,
    get_made_for_you_songs,
    get_trending_songs, GetAllSongsView,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from spotify_app.api.statsView import StatsView
# from spotify_app.api.userView import UserListAPIView

router = DefaultRouter()
urlpatterns = [
    # path('admin/', admin.site.urls),
    path("auth/callback", ClerkAuthCallback.as_view()),
    path("songs/", GetAllSongsView.as_view()),
    path("songs/featured", get_featured_songs),
    path("songs/made-for-you", get_made_for_you_songs),
    path("songs/trending", get_trending_songs),
    path('admin/check/', AdminCheckView.as_view(), name="admin"),
    path('albums/', AlbumViewSet.as_view()),
    path('albums/<int:album_id>/', AlbumDetailAPIView.as_view()),
    path('stats/', StatsView.as_view()),
    path('admin/songs', CreateSongView.as_view(), name='create_song'),
     path('admin/albums', CreateAlbumView.as_view(), name='create-album'),
    path('', include('spotify_app.urls'))

]
