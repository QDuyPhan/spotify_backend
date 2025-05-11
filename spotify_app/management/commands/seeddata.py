from django.core.management.base import BaseCommand
import random
from spotify_app.models.song import Song
from spotify_app.models.album import Album

class Command(BaseCommand):
    help = "Seed database with songs and albums"

    def handle(self, *args, **kwargs):
        Song.objects.all().delete()
        Album.objects.all().delete()

        songs_data = [
            {"title": "PHÓNG ZÌN ZÌN", "artist": "tilinh, Low G", "image_url": "/cover-images/PHÓNG ZÌN ZÌN.jpg", "audio_url": "/songs/PHÓNG ZÌN ZÌN.mp3", "duration": 203},
            {"title": "Thủ Đô Cypher (Remix)", "artist": "Rapital, RPT Orijinn, RZ Ma$, MCK, Low G", "image_url": "/cover-images/Thủ Đô Cypher (Remix).jpg", "audio_url": "/songs/Thủ Đô Cypher (Remix).mp3", "duration": 193},
            {"title": "HOP ON DA SHOW", "artist": "tilinh, Low G", "image_url": "/cover-images/HOP ON DA SHOW.jpg", "audio_url": "/songs/HOP ON DA SHOW.mp3", "duration": 176},
            {"title": "Có Em", "artist": "Madihu, Low G", "image_url": "/cover-images/Có Em.jpg", "audio_url": "/songs/Có Em.mp3", "duration": 219},
            {"title": "Tay To", "artist": "Rapital, PhongKhin, MCK", "image_url": "/cover-images/Tay To.jpg", "audio_url": "/songs/Tay To.mp3", "duration": 165},
            {"title": "XTC (Xích Thêm Chút) (Remix)", "artist": "Rapital, Groovie, MCK, tlinh", "image_url": "/cover-images/Tay To.jpg", "audio_url": "/songs/Tay To.mp3", "duration": 244},
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
            {"title": "Low G", "image_url": "/albums/lowg.jpg", "songs": created_songs[0:5]},

        ]

        for album in album_info:
            new_album = Album.objects.create(
                title=album["title"],
                artist="Various Artists",
                image_url=album["image_url"],
                release_year=2025
            )
            for song in album["songs"]:
                song.album = new_album
                song.save()

        self.stdout.write(self.style.SUCCESS("✅ Database seeded successfully!"))