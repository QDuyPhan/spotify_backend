from rest_framework import serializers
from ..models import Album
from .songserializers import songSerializer


class albumSerializer(serializers.ModelSerializer):
    songs = songSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'image_url', 'release_year','created_at','songs']


