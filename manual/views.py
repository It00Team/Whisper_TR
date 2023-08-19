from django.shortcuts import render, HttpResponse , redirect
import json
from datetime import datetime
from .serializers import AudioSegmentSerializer,MainSerializer,JsonDataSerializer
from .models import MyAudio
from .pyaud import *
from .models import MyAudio, MyAudiomain
from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from pydub import AudioSegment as asp
import whisper
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


def my_function(request):
    return render(request, 'main1.html')


def send_audio(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        name = request.POST.get('name')
        print(name)
        ob = MyAudio(audio_file=audio_file, name=name)
        ob.save()
        return HttpResponse('done')
    return render(request, 'main1.html')



def upload_audio_file(request):
    print('Uploading audio file')
    if request.method == 'POST':
        Aud_file = request.FILES.get('audio_file')
        name1 = request.POST.get('name')
        data = ""
        data_inst = MyAudiomain(name=name1,audio_file=Aud_file)
        data_inst.save()
        print('Uploading audio file is successful')
    return render(request ,'main1.html')
# def manual_segment(request,id=id):
#     def remove_decimal_from_float_str(float_str):
#     # Split the string at the decimal point and take the first part
#         integer_part = float_str.split('.')[0]
#         return integer_part
    
    # print("rAHYGSY")
    # if request.method == 'POST':
    #     audio_file = request.FILES.get('audio_file')
    #     name = audio_file.name
    #     td = str(datetime.now())
    #     nm = str(name)
    #     nm1 = nm.replace(".", "_")
    #     td1 = td.replace(" ", "_")
    #     td1 = td1.replace(".", "_")
    #     td1 = td1.replace(":", "_")
    #     segment = request.POST.get('segment')
    #     # print(type(segment))
    #     fname = nm1+td1
    #     print(fname)
    #     start_time = request.POST.get('start_time')
    #     end_time = request.POST.get('end_time')
    #     int_start = int(remove_decimal_from_float_str(start_time))
    #     int_end = int(remove_decimal_from_float_str(end_time))
    #     int_start = int_start * 1000
    #     int_end = int_end * 1000
    #     print(start_time ,end_time)
    #     # print(audio_file, int_start, int_end)
    #     str_1 = str(audio_file)
    #     r1 = "my_audio/" + str_1
    #     print(r1)

    #     data = upload_file(audio_file,int_start,int_end,name)
    #     print(data)
    #     # new_data =[]
    #     # new_data.append(data)
    #     data_instance1 = MyAudio(name=fname,audio_file=audio_file,description=data)
    #     data_instance1.save()
        
        
    #     print("Uploaded")
        
    #     return render(request ,'main1.html' ,{"data_instance": data})

    # return render(request ,'main1.html')
        






        
       

        # audio = MyAudio.objects.get(audio_file=audio_file)
        # print(audio.id)

        # ob = AudioSegment(start_time=start_time, end_time=end_time)
        # ob.save()
        # // api me bhejna hai

        

        
# def update_content(request, id):
#     if request.user.is_authenticated:
#         audio = MyAudio.objects.get(id=id)
#         print(audio.id)
#         print(audio)
#         if audio.is_modified == False:
#             content = audio.content
#         else:
#             content = audio.updated_content    

#         if request.method == 'POST':
#             updated_content = request.POST.get('updated_content')
#             # is_completed = request.POST.get('completed')
#             # qc = request.POST.get('qc')
                
#             # if is_completed == 'true':
#             #     audio.is_completed = True

#             # if qc == 'true':
#             #     audio.quality_check = True
                    
#             audio.updated_content = updated_content
#             # audio.is_modified = True
#             audio.save()
#             return redirect('table')
#         return render(request, 'main/update.html', {'content': content})
#     return redirect('/') 

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
            # exp = "C:\\tr_2\\media\\my_audio\\" + str(name)
            exp = "C:\\tr_2\\media\\audio_file\\ff1.mp3"

            print(exp)
            serializer.save(name=name,audio_file=exp,description=desc)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
