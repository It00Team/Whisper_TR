from django.db import models

class MyAudio(models.Model):
    # name = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='segment')
    start_time = models.FloatField(null=True)
    end_time = models.FloatField(null=True)
    description = models.TextField(max_length=100000,null=True)
class MyAudiomain(models.Model):
    name = models.CharField(max_length=255,null=True)
    audio_file = models.FileField(upload_to='my_audio',null=True)
    description = models.TextField(max_length=10000000,null=True)

class JsonData(models.Model):
    name = models.CharField(max_length=255,null=True)
    content = models.TextField(null=True)    


# class MyAudioSegment(models.Model):
#     name = models.ForeignKey(MyAudio, on_delete=models.CASCADE)   
#     start_time = models.CharField(max_length=100)
#     end_time = models.CharField(max_length=100)
#     description = models.TextField()
    
