from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

def get_languages():
    pass

def transcribe_diarization_gcs_beta(gcs_uri: str, language, speaker_count):
    
    client_file =r'F:\avyaan\tr_2\main\api.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    speaker_diarization_config = speech.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=speaker_count,
        max_speaker_count=2,
    )

    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code=language,
        sample_rate_hertz=44100,
        enable_word_time_offsets=True,
        diarization_config=speaker_diarization_config,
        audio_channel_count=2,
    )

    audio = speech.RecognitionAudio(
        uri=gcs_uri,
    )

    response = client.long_running_recognize(
        config=recognition_config, audio=audio
    ).result()

    # return response

    sentences = []
    current_sentence = ""
    current_speaker_tag = None
    start_time = None
    # for result in response.results:
    #     for word_info in result.alternatives[0].words:
    #         if word_info.speaker_tag in [2, 1]:  # Only consider speaker 1 and speaker 2
    #             if current_speaker_tag is None:
    #                 current_speaker_tag = word_info.speaker_tag
    #                 start_time = word_info.start_time
    #             if current_speaker_tag == word_info.speaker_tag:
    #                 current_sentence += word_info.word + " "
    #             else:
    #                 sentences.append((current_sentence.strip(), current_speaker_tag, start_time, word_info.end_time))
    #                 current_sentence = word_info.word + " "
    #                 current_speaker_tag = word_info.speaker_tag
    #                 start_time = word_info.start_time

    # sentences.append((current_sentence.strip(), current_speaker_tag, start_time, word_info.end_time))
    # final = ""
    # for sentence, speaker_tag, start_time, end_time in sentences:
    #     final += " Speaker" + str(speaker_tag) +  " : "+ "Start Time: " + str(start_time) +  ' End Time: '+ str(end_time) +  " : " + sentence + "\n" 
    #     # final += " Speaker" + str(speaker_tag) + " : " + sentence + "\n" 
        
    # return final
    for result in response.results:
        for word_info in result.alternatives[0].words:
            if word_info.speaker_tag in [2, 1]:  # Only consider speaker 1 and speaker 2
                if current_speaker_tag is None:
                    current_speaker_tag = word_info.speaker_tag
                if current_speaker_tag == word_info.speaker_tag:
                    current_sentence += word_info.word + " "
                else:
                    sentences.append((current_sentence.strip(), current_speaker_tag))
                    current_sentence = word_info.word + " "
                    current_speaker_tag = word_info.speaker_tag

    sentences.append((current_sentence.strip(), current_speaker_tag))
    
    final = ""
    for sentence, speaker_tag in sentences:
        final += "Speaker " + str(speaker_tag) + ": " + sentence + "\n"

    return final

        