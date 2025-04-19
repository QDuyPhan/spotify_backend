from django.db import models
import uuid
# Create your models here.
class user(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clerk_id = models.CharField(max_length=100, blank=True, null=True, unique=True) 
    fullName = models.CharField(max_length=255)
    imageUrl = models.URLField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_authenticated(self):
        return True
