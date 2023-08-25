from django.db import models
from django.contrib.auth.models import User

class Audio(models.Model):
    name = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='audio_file/')
    type = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    language = models.CharField(max_length=100)
    quality_check = models.BooleanField(default=False)
    content = models.TextField()
    is_modified = models.BooleanField(default=False)
    updated_content = models.TextField(null=True, blank=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
class GoogleAudio(models.Model):
    name = models.CharField(max_length=100)
    Audio_File = models.FileField(upload_to='audio/')
    description = models.TextField()

