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
from spotify_app.api.albumView import AlbumSongsOfUserView, AlbumViewSet, AlbumDetailAPIView, CreateAlbumByUserView, CreateAlbumView, DeleteAlbumView, ListAlbumsOfUserView
from spotify_app.api.authenticationView import *
from spotify_app.api.songView import (
    AddSongToAlbumView,
    CreateSongView,
    DeleteSongView,
    FavoriteSongView,
    ListFavoriteSongsView,
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
    path("songs/", GetAllSongsView.as_view(), name='get-all-songs'),
    path("songs/featured/", get_featured_songs, name='featured-songs'),
    path("songs/made-for-you/", get_made_for_you_songs, name='made-for-you-songs'),
    path("songs/trending/", get_trending_songs, name='trending-songs'),
    path('admin/check/', AdminCheckView.as_view(), name="admin"),
    path('albums/', AlbumViewSet.as_view(), name='albums'),
    path('albums/<int:album_id>/', AlbumDetailAPIView.as_view(), name='album-detail'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('admin/songs/', CreateSongView.as_view(), name='create-song'),
    path('admin/albums/', CreateAlbumView.as_view(), name='create-album'),
    path('songs/<int:id>/delete/', DeleteSongView.as_view(), name='delete-song'),
    path('albums/<int:id>/delete/', DeleteAlbumView.as_view(), name='delete-album'),
    path('albums/user/create/', CreateAlbumByUserView.as_view(), name='user-create-album'),
    path("albums/user/", ListAlbumsOfUserView.as_view(), name="list-user-albums"),
    path("songs/user-albums/add-song/", AddSongToAlbumView.as_view(), name="add-song-to-album"),
    path('albums/<int:album_id>/songs/', AlbumSongsOfUserView.as_view(), name='album-songs-of-user'),
    path('songs/favorite/', FavoriteSongView.as_view(), name='favorite-song'),
    path('songs/favorite/list/', ListFavoriteSongsView.as_view(), name='favorite-song-list'),
    path('', include('spotify_app.urls'))
]
