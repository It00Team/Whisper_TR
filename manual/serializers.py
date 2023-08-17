from rest_framework import serializers
from .models import MyAudio, MyAudiomain , JsonData
# from .models import JsonData

class JsonDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = JsonData
        fields = '__all__'

class AudioSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAudio
        fields = '__all__'
class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyAudiomain
        fields = '__all__'
