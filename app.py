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

def get_direct_download_link(video_url):
    """
    Convert Google Drive link to direct download link if applicable.
    """
    if "drive.google.com" in video_url:
        try:
            if "/file/d/" in video_url:
                file_id = video_url.split("/file/d/")[1].split("/")[0]
            elif "id=" in video_url:
                file_id = video_url.split("id=")[1].split("&")[0]
            else:
                raise ValueError("Invalid Google Drive link format")
            direct_link = f"https://drive.google.com/uc?id={file_id}&export=download"
            print(f"Converted Google Drive link to: {direct_link}")  # Debugging
            return direct_link
        except Exception as e:
            raise ValueError(f"Error processing Google Drive link: {e}")
    return video_url  # Return the original URL if not a Google Drive link

def download_video(video_url):
    """
    Download video from the provided URL and return its local file path.
    """
    video_hash = hashlib.md5(video_url.encode()).hexdigest()  # Generate unique file name
    video_path = os.path.join(DOWNLOAD_FOLDER, f"{video_hash}.mp4")
    response = requests.get(video_url, stream=True)
    if response.status_code != 200:
        raise Exception("Failed to download video")
    with open(video_path, 'wb') as video_file:
        for chunk in response.iter_content(chunk_size=1024):
            video_file.write(chunk)
    print(f"Video downloaded to: {video_path}")  # Debugging
    return video_path

def transcribe(source, mimetype=None):
    """
    Transcribe video/audio using Deepgram.
    """
    try:
        response = dg_client.transcription.sync_prerecorded(
            source=source,
            options={'punctuate': True, 'timestamps': True}
        )
        return response
    except Exception as e:
        raise Exception(f"Transcription failed: {str(e)}")

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    """
    Handle transcription requests.
    """
    try:
        # Parse request JSON
        data = request.json
        video_url = data.get('video_url')
        direct_transcription = data.get('direct_transcription', False)

        if not video_url:
            return jsonify({'error': 'Video URL is required'}), 400

        # converts given link into downloadable link
        video_url = get_direct_download_link(video_url)

        # Option 1: This option handles direct transcription, use "direct_transcription": true in body json if you wish to have live transcription
        if direct_transcription:
            print(f"Performing direct transcription for: {video_url}")  # Debugging
            transcription = transcribe({'url': video_url})
            return jsonify(transcription), 200

        # Option 2: This option handles direct transcription, use "direct_transcription": false in body json if you wish to have the video locally
        video_path = download_video(video_url)
        with open(video_path, 'rb') as video_file:
            transcription = transcribe({'buffer': video_file, 'mimetype': 'video/mp4'})
        
        #This lime of code below deletes the video file after transcript, please keep it as a comment/delete it if you wish to keep the transcribed video.
        # os.remove(video_path)

        return jsonify(transcription), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)

