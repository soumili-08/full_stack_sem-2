from django.db import models
from django.contrib.auth.models import User

# Song Model
class Song(models.Model):
    name = models.CharField(max_length=2000)
    singer = models.CharField(max_length=2000)
    tags = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='media')
    song = models.FileField(upload_to='media')
    movie = models.CharField(max_length=1000, default="")
    mood = models.CharField(max_length=100, choices=[('happy', 'Happy'), ('sad', 'Sad'), ('energetic', 'Energetic'), ('romantic', 'Romantic'), ('chill', 'Chill')], default='happy')

    def __str__(self):
        return self.name

# Playlist Model (Assuming you're building playlist functionality)
class Playlist(models.Model):
    name = models.CharField(max_length=2000)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# UserFav Model - To track favorite songs of users
class UserFav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.song.name}'



class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.playlist.name} - {self.song.name}"


class Karaoke(models.Model):
    name = models.CharField(max_length=255)
    lyrics = models.TextField()
    background_song = models.FileField(upload_to='karaoke_songs',max_length=900)
    image = models.ImageField(upload_to='karaoke_images')

    def __str__(self):
        return self.name