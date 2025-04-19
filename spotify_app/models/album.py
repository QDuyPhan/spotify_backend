from django.db import models

# Create your models here.
# class album(models.Model):
#     title = models.CharField(max_length=255)
#     artist = models.CharField(max_length=255)
#     imagineUrl = models.URLField()
#     releaseYear = models.IntegerField()
#     songs = models.ManyToManyField(
#         song,
#         related_name='albums'
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     def __str__(self):
#         return f"{self.title} - {self.artist} - {self.imagineUrl} - {self.releaseYear} - {self.songs} - {self.created_at} - {self.updated_at}"
    
class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    release_year = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title