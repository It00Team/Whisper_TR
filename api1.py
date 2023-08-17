import os
from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)

# Load the Whisper ASR model
model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Get the uploaded audio file from the request
        # audio_file = request.files['audio']
        # Save the audio file temporarily
        file_name = request.args.get('file_name')
        temp_path = 'C:\\tr_2\\media\\segment\\' + file_name
        # audio_file.save(temp_path)

        # Transcribe the audio
        result = model.transcribe(temp_path)

        # Delete the temporary audio file
        # os.remove(temp_path)

        # Return the transcription result
        return jsonify({"text": result["text"]})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
