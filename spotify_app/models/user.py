from django.db import models
import uuid
# Create your models here.
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clerk_id = models.CharField(max_length=100, blank=True, null=True, unique=True) 
    fullName = models.CharField(max_length=255)
    imageUrl = models.URLField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorite_albums = models.ManyToManyField('Album', related_name='liked_by_users', blank=True)
    favorite_songs = models.ManyToManyField('Song', related_name='liked_by_users', blank=True)
    