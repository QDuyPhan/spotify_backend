from django.db import models
from django.utils import timezone
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image_url = models.URLField(null=True)
    audio_url = models.URLField()
    duration = models.PositiveIntegerField()
    album = models.ForeignKey("Album", null=True, blank=True, on_delete=models.SET_NULL, related_name='songs')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)