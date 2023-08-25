from django.shortcuts import render, HttpResponse , redirect
import json
from datetime import datetime
from .serializers import AudioSegmentSerializer,MainSerializer,JsonDataSerializer,WisperSerializer
from .models import MyAudio
from .models import MyAudio, MyAudiomain
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pydub import AudioSegment as asp
import whisper


def my_function(request):
    return render(request, 'main1.html')
def my_function_new(request):
    return render(request, 'index.html')
class Whisper_TR(APIView):
    def post(self, request,format=None):
        serializer = WisperSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            # name = serializer.validated_data['name']
            # print(name)
            audio = request.FILES['audio']
            print(type(audio))
            audio_path = "C:\\Users\\91722\\Desktop\\git vala folder\\Whisper_TR\\media\\" + str(audio)
            with open(audio_path, 'wb') as audio_file:
                audio_file.write(request.FILES['audio'].read())
            model = whisper.load_model("base")
            result = model.transcribe(audio_path)
            data = result["text"]
            # audio = request.FILES('audio')
            # audio = serializer.validated_data['audio']
            # print(audio)
            print("saving")
            serializer.save(description="raju")
            print("done")
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateJsonFileView(APIView):
    def post(self, request, format=None):
        serializer = JsonDataSerializer(data=request.data)        # print(serializer)
        if serializer.is_valid():
            json_data = serializer.data
            print(json_data['content'])
            json_content = json.dumps(json_data['content'], indent=4)            
            response = HttpResponse(json_content, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="audio_transcription.json"'
            return response
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class manseg(APIView):
    def post(self, request, format=None):
        serializer = AudioSegmentSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            strt = serializer.validated_data['start_time']
            end = serializer.validated_data['end_time']
            audio = serializer.validated_data['audio_file']

            print(audio)
            def miliseconds_to_hh_mm_ss(seconds):
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                seconds = int(seconds % 60)
                # milliseconds = int((seconds - int(seconds)) * 1000)
                con  = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
                return con
            started = miliseconds_to_hh_mm_ss(strt)
            ended = miliseconds_to_hh_mm_ss(end)
            print(started)
            print(ended)
            audio_path = "C:\\tr_2\\media\\audio_file\\" + str(audio)
            with open(audio_path, 'wb') as audio_file:
                audio_file.write(request.FILES['audio_file'].read())
            a1 = "C:\\tr_2\\media\\audio_file\\" + str(audio)
            file_take = asp.from_file(a1)
            # set_frame_rate
            sample_rate = file_take.frame_rate
            samplerate = file_take.set_frame_rate(44100)
            print(samplerate)
            print(type(samplerate))
            samplerate.export(f'C:\\Users\\91722\\Desktop\\git vala folder\\Whisper_TR\\media\\{audio}', format="wav")
            # samplerate.export(r'C:\\Users\\91722\\Desktop\\git vala folder\\Whisper_TR\\media\\audio\\raju.wav', format="wav")
            print("Sample Rate:", sample_rate, "Hz")
            z1 = int(strt * 1000)
            z2 = int(end * 1000)
            segment = file_take[z1 : z2]
            date = str(datetime.now())
            fdate = date.replace(' ', '_').replace('.', '_').replace(':', '_').replace('-', '_')
            exp = r'C:\\tr_2\\media\\segment\\'+str(audio)+fdate+".mp3"
            segment.export(exp, format="mp3")
            model = whisper.load_model("base")
            result = model.transcribe(exp)
            raju = result["text"]
            data = "Speaker : " +"Start_time : "+str(started) +" End_time : "+ str(ended) +" "+ "Text : " + str(raju)
            print(data)
            maindata = {"data": data}
            serializer.save(audio_file=exp,description=data)
            return Response(maindata, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class finaldata(APIView):
    def post(self, request, format=None):
        serializer = MainSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            desc = serializer.validated_data['description']
            print(name)
            print(desc)
            exp = "C:\\tr_2\\media\\my_audio\\" + str(name)
            print(exp)
            serializer.save(name=name,audio_file=exp,description=desc)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
