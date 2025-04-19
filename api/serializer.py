from rest_framework import serializers
from .models import user
from .models import Song
from .models import message
from .models import Album

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'

class songSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class albumSerializer(serializers.ModelSerializer):
    songs = songSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        fields = '__all__'

class messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'