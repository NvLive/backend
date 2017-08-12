from django.contrib import admin
from .models import Broadcast, Show

admin.site.register([Broadcast, Show])
