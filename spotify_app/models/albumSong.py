from django.db import models


class AlbumSong(models.Model):
    album = models.ForeignKey("spotify_app.Album", on_delete=models.CASCADE)
    song = models.ForeignKey("spotify_app.Song", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('album', 'song')

