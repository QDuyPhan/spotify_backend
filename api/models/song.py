from django.db import models

# Create your models here.
class song(models.Model):
    title = models.CharField(max_length=255,unique=True)
    artist = models.CharField(max_length=255)
    imagineUrl = models.CharField(max_length=255)
    audioUrl = models.CharField(max_length=255)
    duration = models.DurationField(("Duration"))
    albumid = models.ForeignKey(
        'album',
        on_delete=models.SET_NULL,
        null = True,
        blank = True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title} - {self.artist} - {self.imagineUrl} - {self.audioUrl} - {self.duration} - {self.albumid} - {self.created_at} - {self.updated_at}"
    