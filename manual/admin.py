from django.contrib import admin
from .models import MyAudio, MyAudiomain, JsonData

@admin.register(MyAudio)
class MyAudioAdmin(admin.ModelAdmin):
    list_display = ['id', 'audio_file', 'start_time', 'end_time']

@admin.register(MyAudiomain)
class MyAudiomainAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'audio_file', 'description']

@admin.register(JsonData)
class MydatamainAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content']
