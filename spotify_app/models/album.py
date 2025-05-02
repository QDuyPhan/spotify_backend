from django.db import models

from spotify_app.models.user import User
from spotify_app.models.song import Song
    
class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image_url = models.CharField(max_length=1024)
    release_year = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums', null=True, blank=True)
    songs = models.ManyToManyField(Song, through='AlbumSong', related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title