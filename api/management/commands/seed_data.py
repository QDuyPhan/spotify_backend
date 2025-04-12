from django.core.management.base import BaseCommand
import random
from api.models.song import Song
from api.models.album import Album

class Command(BaseCommand):
    help = "Seed database with songs and albums"

    def handle(self, *args, **kwargs):
        Song.objects.all().delete()
        Album.objects.all().delete()

        songs_data = [
            {"title": "City Rain", "artist": "Urban Echo", "image_url": "/cover-images/7.jpg", "audio_url": "/songs/7.mp3", "duration": 39},
            {"title": "Neon Lights", "artist": "Night Runners", "image_url": "/cover-images/5.jpg", "audio_url": "/songs/5.mp3", "duration": 36},
            {"title": "Urban Jungle", "artist": "City Lights", "image_url": "/cover-images/15.jpg", "audio_url": "/songs/15.mp3", "duration": 36},
            {"title": "Neon Dreams", "artist": "Cyber Pulse", "image_url": "/cover-images/13.jpg", "audio_url": "/songs/13.mp3", "duration": 39},
            {"title": "Summer Daze", "artist": "Coastal Kids", "image_url": "/cover-images/4.jpg", "audio_url": "/songs/4.mp3", "duration": 24},
            {"title": "Ocean Waves", "artist": "Coastal Drift", "image_url": "/cover-images/9.jpg", "audio_url": "/songs/9.mp3", "duration": 28},
            {"title": "Crystal Rain", "artist": "Echo Valley", "image_url": "/cover-images/16.jpg", "audio_url": "/songs/16.mp3", "duration": 39},
            {"title": "Starlight", "artist": "Luna Bay", "image_url": "/cover-images/10.jpg", "audio_url": "/songs/10.mp3", "duration": 30},
            {"title": "Stay With Me", "artist": "Sarah Mitchell", "image_url": "/cover-images/1.jpg", "audio_url": "/songs/1.mp3", "duration": 46},
            {"title": "Midnight Drive", "artist": "The Wanderers", "image_url": "/cover-images/2.jpg", "audio_url": "/songs/2.mp3", "duration": 41},
            {"title": "Moonlight Dance", "artist": "Silver Shadows", "image_url": "/cover-images/14.jpg", "audio_url": "/songs/14.mp3", "duration": 27},
            {"title": "Lost in Tokyo", "artist": "Electric Dreams", "image_url": "/cover-images/3.jpg", "audio_url": "/songs/3.mp3", "duration": 24},
            {"title": "Neon Tokyo", "artist": "Future Pulse", "image_url": "/cover-images/17.jpg", "audio_url": "/songs/17.mp3", "duration": 39},
            {"title": "Purple Sunset", "artist": "Dream Valley", "image_url": "/cover-images/12.jpg", "audio_url": "/songs/12.mp3", "duration": 17},
        ]

        created_songs = []

        for data in songs_data:
            song = Song.objects.create(
                title=data["title"],
                artist=data["artist"],
                image_url=data["image_url"],
                audio_url=data["audio_url"],
                plays=random.randint(0, 5000),
                duration=data["duration"]
            )
            created_songs.append(song)

        album_info = [
            {"title": "Urban Nights", "image_url": "/albums/1.jpg", "songs": created_songs[0:4]},
            {"title": "Coastal Dreaming", "image_url": "/albums/2.jpg", "songs": created_songs[4:8]},
            {"title": "Midnight Sessions", "image_url": "/albums/3.jpg", "songs": created_songs[8:11]},
            {"title": "Eastern Dreams", "image_url": "/albums/4.jpg", "songs": created_songs[11:14]},
        ]

        for album in album_info:
            new_album = Album.objects.create(
                title=album["title"],
                artist="Various Artists",
                image_url=album["image_url"],
                release_year=2024
            )
            for song in album["songs"]:
                song.album = new_album
                song.save()

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))