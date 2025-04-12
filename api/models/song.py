from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255,null=True)
    audio_url = models.CharField(max_length=255)
    duration = models.IntegerField()
    plays = models.IntegerField(default=0)
    album = models.ForeignKey("Album", on_delete=models.SET_NULL, null=True, blank=True, related_name="songs")

    def __str__(self):
        return self.title