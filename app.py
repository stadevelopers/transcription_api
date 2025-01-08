from flask import Flask, request, jsonify
import requests
import os
import hashlib
from deepgram import Deepgram

# Initialize Flask app
app = Flask(__name__)

# Configuration
DEEPGRAM_API_KEY = '3d4728611a2424222b04c90f9f6db374ebbad040'  # Replace with your Deepgram API key
DOWNLOAD_FOLDER = './videos'  # Folder to store downloaded videos
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Initialize Deepgram client
dg_client = Deepgram(DEEPGRAM_API_KEY)

def convert_to_downloadable_link(video_url):
    """
    Convert a video URL to a direct download link if applicable (e.g., for Google Drive links).
    """
    if "drive.google.com" in video_url and "/file/d/" in video_url:
        file_id = video_url.split("/file/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?id={file_id}&export=download"
    elif "drive.google.com" in video_url and "id=" in video_url:
        file_id = video_url.split("id=")[1].split("&")[0]
        return f"https://drive.google.com/uc?id={file_id}&export=download"
    return video_url  # Return the original URL for non-Google Drive links

def convert_to_downloadable_link(video_url):
    """
    Convert video URL to a direct download link if it's a Google Drive or Dropbox link.
    """
    if "drive.google.com" in video_url:
        if "/file/d/" in video_url:
            file_id = video_url.split("/file/d/")[1].split("/")[0]
            return f"https://drive.google.com/uc?id={file_id}&export=download"
        elif "id=" in video_url:
            file_id = video_url.split("id=")[1].split("&")[0]
            return f"https://drive.google.com/uc?id={file_id}&export=download"
    
    elif "dropbox.com" in video_url:
        return video_url.replace("www.dropbox.com", "dl.dropboxusercontent.com").split('?')[0]
    
    return video_url  # Return original URL for other links

def transcribe(source):
    """
    Transcribe video/audio using Deepgram.
    """
    response = dg_client.transcription.sync_prerecorded(
        source=source,
        options={'punctuate': True, 'timestamps': True}
    )
    return response

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    """
    Handle transcription requests.
    """
    try:
        data = request.json
        video_url = data.get('video_url')
        direct_transcription = data.get('direct_transcription', False)

        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400

        # Option 1: Direct transcription without downloading
        if direct_transcription:
            transcription = transcribe({'url': video_url})
            return jsonify(transcription), 200

        # Option 2: Download video and transcribe locally
        video_path = download_video(video_url)
        with open(video_path, 'rb') as video_file:
            transcription = transcribe({'buffer': video_file, 'mimetype': 'video/mp4'})
        
        # Uncomment the following line to delete the video after transcription
        # os.remove(video_path)

        return jsonify(transcription), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
