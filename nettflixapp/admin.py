from django.contrib import admin
from .models import Movie, Show, UserList

# Register your models here.
admin.site.register(Movie)
admin.site.register(Show)
admin.site.register(UserList)


