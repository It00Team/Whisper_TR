import requests
from pydub import AudioSegment
from datetime import datetime
import whisper 

def upload_file(audio_file,int_start,int_end,name):
    file_take = AudioSegment.from_mp3(audio_file)
    segment = file_take[int_start : int_end]
    print(type(audio_file))
    td = str(datetime.now())
    nm = str(name)
    nm1 = nm.replace(".", "_")
    td1 = td.replace(" ", "_")
    td1 = td1.replace(".", "_")
    td1 = td1.replace(":", "_")
    segment.export(r'C:\\tr_2\\media\segment\\'+ f'{nm1}_{td1}.mp3', format="mp3")
    print("successfully sent to API server")
    # api_url = "http://127.0.0.1:5000/transcribe"  # Replace with your API URL
    # audio_file_path = r'C:\\tr_2\\media\segment\\'+ f'{nm1}_{td1}.mp3'  # Replace with the actual path to your audio file

    # files = {'audio': open(audio_file_path, 'rb')}

    # try:
    # Send the POST request to the Flask API
        # response = requests.post(api_url, files=files)

    # Check if the request was successful
    #     if response.status_code == 200:
    #         result = response.json()
    #         transcription = result.get('text', 'Transcription not available')
    #         try :
    #             raju = f'Transcription result: {transcription}'
    #         except Exception as e :
    #             print(e)
    #             raju="no transcription"
    #     else:
    #         print(f'Error: {response.status_code} - {response.text}')

    # except requests.exceptions.RequestException as e:
    #     print(f'Error sending request: {e}')
    model = whisper.load_model("base")
    result = model.transcribe(r'C:\\tr_2\\media\segment\\'+ f'{nm1}_{td1}.mp3')
    raju = result["text"]
    print(raju)
    return raju