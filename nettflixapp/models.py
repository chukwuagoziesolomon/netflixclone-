from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from PIL import Image
import os
from django.conf import settings

  

# Create your models here.
GENRE_CHOICES = [
    ('action', 'Action'),
    ('comedy', 'Comedy'),
    ('drama', 'Drama'),
    ('horror', 'Horror'),
    ('romance', 'Romance'),
    ('science_fiction', 'Science Fiction'),
    ('fantasy', 'Fantasy'),
]

class Movie(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(
        upload_to='posters/',
        default='posters/default.jpg',
        
    )
    release_date = models.DateField(default='2023-01-01')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='action')
    length = models.PositiveIntegerField(default=120)
    image_card = models.ImageField(
        upload_to='movie_images/',
        default='movie_images/default.jpg',
    
        help_text='Image should have a 2:3 aspect ratio'
    )
    image_cover = models.ImageField(
        upload_to='movie_images/',
        default='movie_images/default.jpg',
        help_text='Image should have a 16:9 aspect ratio'
    )
    video = models.FileField(upload_to='movie_videos/', default='movie_videos/default.mp4')
    movies_views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def save(self, *args, **kwargs):
        # Process images before saving
        if self.image_card:
            img = Image.open(self.image_card)
            # Resize to standard dimensions (200x300 for 2:3 ratio)
            img = img.resize((200, 300), Image.Resampling.LANCZOS)
            img.save(self.image_card.path)
            
        if self.image_cover:
            img = Image.open(self.image_cover)
            # Resize to standard dimensions (1920x1080 for 16:9 ratio)
            img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            img.save(self.image_cover.path)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Show(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(max_length=200)
    description = models.TextField()
    poster = models.ImageField(
        upload_to='posters/',
        default='posters/default.jpg',
    
    )
    release_date = models.DateField(default='2023-01-01')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='action')
    seasons = models.PositiveIntegerField(default=1)
    image_card = models.ImageField(
        upload_to='show_images/',
        default='show_images/default.jpg',
        help_text='Image should have a 2:3 aspect ratio'
    )
    image_cover = models.ImageField(
        upload_to='show_images/',
        default='show_images/default.jpg',
        
        help_text='Image should have a 16:9 aspect ratio'
    )
    video = models.FileField(upload_to='show_videos/', default='show_videos/default.mp4')
    show_views = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)

    def save(self, *args, **kwargs):
        # Process images before saving
        if self.image_card:
            img = Image.open(self.image_card)
            # Resize to standard dimensions (200x300 for 2:3 ratio)
            img = img.resize((200, 300), Image.Resampling.LANCZOS)
            img.save(self.image_card.path)
            
        if self.image_cover:
            img = Image.open(self.image_cover)
            # Resize to standard dimensions (1920x1080 for 16:9 ratio)
            img = img.resize((1920, 1080), Image.Resampling.LANCZOS)
            img.save(self.image_cover.path)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie', 'show')

    def __str__(self):
        if self.movie:
            return f"{self.user.username} - {self.movie.title}"
        elif self.show:
            return f"{self.user.username} - {self.show.title}"
        return f"{self.user.username} - Empty List"


class Movielist(models.Model):
    user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

