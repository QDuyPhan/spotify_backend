from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255, null=True)
    release_year = models.IntegerField()

    def __str__(self):
        return self.title