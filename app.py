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
    Convert video links into direct download links if applicable.
    Supports Google Drive and Dropbox. Returns original URL for other links.
    """
    if "drive.google.com" in video_url:
        # Extract the file ID from the Google Drive link
        file_id = (
            video_url.split("/file/d/")[1].split("/")[0]
            if "/file/d/" in video_url
            else video_url.split("id=")[1].split("&")[0]
        )
        # Return the downloadable link for Google Drive
        return f"https://drive.google.com/uc?id={file_id}&export=download"
    
    if "dropbox.com" in video_url:
        # Convert Dropbox shareable link to direct download link
        return video_url.replace("www.dropbox.com", "dl.dropboxusercontent.com").split('?')[0]
    
    # Return original URL for non-Google Drive and non-Dropbox links
    return video_url

def download_video(video_url):
    """
    Download video from the provided URL and return its local file path.
    """
    video_url = get_direct_download_link(video_url)  # Ensure the link is downloadable
    video_hash = hashlib.md5(video_url.encode()).hexdigest()  # Generate unique file name
    video_path = os.path.join(DOWNLOAD_FOLDER, f"{video_hash}.mp4")
    
    response = requests.get(video_url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Failed to download video. Status code: {response.status_code}")
    
    with open(video_path, 'wb') as video_file:
        for chunk in response.iter_content(chunk_size=1024):
            video_file.write(chunk)
    
    return video_path

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
            transcription = transcribe({'url': get_direct_download_link(video_url)})
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
