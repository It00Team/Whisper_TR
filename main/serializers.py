from rest_framework import serializers
from .models import GoogleAudio

class AudioService(serializers.ModelSerializer):
    class Meta:
        model = GoogleAudio
        fields = '__all__'
        