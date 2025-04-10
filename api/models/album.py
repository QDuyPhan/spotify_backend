from django.db import models
from api.models import song

# Create your models here.
class album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    imagineUrl = models.URLField()
    releaseYear = models.IntegerField()
    songs = models.ManyToManyField(
        song,
        related_name='albums'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} - {self.artist} - {self.imagineUrl} - {self.releaseYear} - {self.songs} - {self.created_at} - {self.updated_at}"
    