from django.contrib import admin
from .models import Song, UserFav

# Register your models here.

admin.site.register(Song)
admin.site.register(UserFav)

