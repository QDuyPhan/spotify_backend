from django.db import models
from django.utils import timezone
class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image_url = models.URLField(null=True)
    release_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)