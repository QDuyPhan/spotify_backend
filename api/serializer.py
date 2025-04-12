from rest_framework import serializers
from .models import user
from .models import song
from .models import message
from .models import Album

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = '__all__'
        
        def create(self, validated_data):
            user = user.objects.create_user(**validated_data)
            return user

class songSerializer(serializers.ModelSerializer):
    class Meta:
        model = song
        fields = '__all__'

class albumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class messageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = '__all__'                