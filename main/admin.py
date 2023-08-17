from django.contrib import admin
from .models import * 

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'audio_file', 'type', 'language', 'quality_check']
