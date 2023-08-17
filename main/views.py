from django.shortcuts import render , redirect, HttpResponse ,HttpResponseRedirect
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.models import User
from .uploadFile  import *
from .deleteFile  import *
from .segment  import *
from .speakerFile  import *
import os
from django.core.files.storage import default_storage
import json
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from pydub import AudioSegment
import shutil
from datetime import timedelta

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = User.objects.get(username=username)
                if user is  None :
                    messages.error(request, "User does not exist")
                    return redirect('login')
                
                user = authenticate(username=username, password=password)
                if user is None :
                    messages.error(request, " Invalid Username or Password")
                    return redirect('login')
                
                login(request, user)
                return redirect('home')
            
            return redirect('login')
        form = LoginForm()
        return render(request , 'main/login.html' , {'form': form})

    return redirect('/login/')

def user_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request , 'User signed up successfully')
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})

# add me 
def home(request):
    return render(request, 'main/home.html')


def update_content(request, id):
    if request.user.is_authenticated:
        audio = Audio.objects.get(id=id)
        if audio.is_modified == False:
            content = audio.content
        else:
            content = audio.updated_content    

        if request.method == 'POST':
            updated_content = request.POST.get('updated_content')
            is_completed = request.POST.get('completed')
            qc = request.POST.get('qc')
                
            if is_completed == 'true':
                audio.is_completed = True

            if qc == 'true':
                audio.quality_check = True
                    
            audio.updated_content = updated_content
            audio.is_modified = True
            audio.save()
            return redirect('table')
        return render(request, 'main/update.html', {'content': content})
    return redirect('/')


def segment(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        language = request.POST.get('language')
        name = os.path.basename(audio_file.name)    
        type = (os.path.splitext(name)[-1])
        print(language)

        ob1 = Audio(language=language, name=name, type=type, audio_file=audio_file, userId=request.user)
        ob1.save()

        break_point = 1
        count = 20000
        song = AudioSegment.from_mp3(audio_file)
        print(song)


        x = song.duration_seconds *1000
        print(x)

        final_result = ""
        folder = 'C:\\tr_2\\media\\segment'

        start_time = 0
        end_time = 20
        while break_point*count<=x:
            print("Starting")
            croped = song[(break_point-1)*count : break_point*count]
            croped_name = os.path.join(folder, f"{name}_{break_point}")
            croped.export(croped_name, format="mp3")

            # file_path = croped_name

            client_file = r'C:\\tr_2\\main\\new.json'
            credentials = service_account.Credentials.from_service_account_file(client_file)
            client = storage.Client(credentials=credentials)

            bucket = client.bucket('avyaan_mgmt')
            blob = bucket.blob(croped_name)
            blob.upload_from_filename(croped_name)
            print('Uploaded audio file:', croped_name)

            print(croped_name)

            uri = 'gs://avyaan_mgmt/' + croped_name 
            sentences = transcribe_diarization_gcs_beta(uri, language, 1)

            delete_file('avyaan_mgmt', croped_name)
            print('Deleted file:')
            s = get_time_hh_mm_ss(start_time)
            e = get_time_hh_mm_ss(end_time)
            # final_result+= f"Start Time : {s} : End Time {e} : {sentences} "
            final_result+= f"{e} : {sentences} "

            start_time = start_time + 20
            end_time = end_time + 20
            break_point = break_point + 1
        print(final_result)


        ob1.content = final_result
        ob1.save()

        return render(request, 'main/segment.html', {'content': final_result})
    print("Success")
    return render(request , 'main/segment.html')



def audio(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio_file')
        language = request.POST.get('language')
        speaker_count = int(request.POST.get('speaker_count'))
        name = os.path.basename(audio_file.name)    
        type = (os.path.splitext(name)[-1])
        print(language)

        ob1 = Audio(language=language, name=name, type=type, audio_file=audio_file, userId=request.user)
        ob1.save()

        audio_file_name = os.path.basename(audio_file.name)
        file_path = 'C:\\tr_2\media\\audio_file\\' + audio_file_name

        client_file = r'C:\\tr_2\\main\\new.json'
        credentials = service_account.Credentials.from_service_account_file(client_file)
        client = storage.Client(credentials=credentials)

        bucket = client.bucket('avyaan_mgmt')
        blob = bucket.blob(file_path)
        blob.upload_from_filename(file_path)
        print('Uploaded audio file:', audio_file_name)

        print(audio_file_name)

        uri = 'gs://avyaan_mgmt/' + file_path 
        sentences = speaker_speech_to_text(uri, language)

        delete_file('avyaan_mgmt', file_path)
        print('Deleted file:')

        ob1.content = sentences
        ob1.save()
        #

        return render(request, 'main/audio.html', {'sentences': sentences})
    return render(request , 'main/audio.html')


        
#new code 
def table(request):
    audio = Audio.objects.filter(userId=request.user.id)
    return render(request, 'main/table.html', {'audio': audio})

def show_data(request):
    audio = Audio.objects.all()
    json_data = serializers.serialize('json', audio)
    formatted_json = json.dumps(json.loads(json_data), indent=4)
    return HttpResponse(formatted_json, content_type='application/json')

def user_logout(request):
    logout(request)
    return redirect('login')

#new code
def my_json(request, id):
    audio = get_object_or_404(Audio, id=id)
    myname = audio.name
    json_data = serializers.serialize('json', [audio])
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{myname}_{id}.json"'
    return response


def get_time_hh_mm_ss(sec):
    # create timedelta and convert it into string
    td_str = str(timedelta(seconds=sec))
    print('Time in seconds:', sec)

    # split string into individual component
    x = td_str.split(':')
    print('Time in hh:mm:ss:', x[0], 'Hours', x[1], 'Minutes', x[2], 'Seconds')
    return f'{x[0]}:{x[1]}:{x[2]}'

#new code
def download_json(request, id):
    try:
        audio = Audio.objects.get(id=id)
        content = audio.content
        json_data = {'data': content}
        final_data = json.dumps(json_data, ensure_ascii=False, indent=4)
        response = HttpResponse(final_data, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="audio_data_{id}.json"'
        return response
    except Audio.DoesNotExist:
        return HttpResponse("Audio not found", status=404)


