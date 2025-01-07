Video Transcription API

A Python-based Flask API for video transcription using the Deepgram API. This API supports transcribing video files from URLs, including Google Drive links, and provides transcription results in JSON format with word-level timestamps.

Features:

Transcription Options:
Direct Transcription: Transcribe audio directly from a URL.
Local Transcription: Download the video to the server before transcription.
Supports Google Drive Links: Converts Google Drive sharing links into direct download links automatically.
Word-Level Timestamps: Provides detailed transcription results with timestamps for each word.
Health Check Endpoint: A simple /health endpoint for monitoring the app's availability.
Error Handling: Handles invalid URLs, unsupported formats, and other issues gracefully.
Getting Started

Prerequisites:

Python 3.10+
A Deepgram API key (sign up at deepgram.com for an API key)
Installation:

Clone the repository: git clone https://github.com/your-username/transcription-api.git cd transcription-api

Install dependencies: pip install -r requirements.txt

Set up a folder for video downloads: mkdir videos

Add your Deepgram API key: Replace the placeholder DEEPGRAM_API_KEY in app.py with your actual API key.

Usage

Run the API Locally:

Start the Flask app: python app.py

The app will run on: http://127.0.0.1:5000

Endpoints:

/transcribe
Method: POST
Description: Transcribes video files from a URL.
Request Body (JSON): { "video_url": "https://example.com/video.mp4", "direct_transcription": true }
video_url (required): The URL of the video file (supports Google Drive links).
direct_transcription (optional):
true for direct transcription without downloading the video.
false (default) to download the video locally before transcription.
Response (Success): { "results": { "channels": [ { "alternatives": [ { "transcript": "Hello, this is a test transcription.", "timestamps": [ ["Hello", 0.0, 0.5], ["this", 0.5, 1.0], ["is", 1.0, 1.5], ["a", 1.5, 1.8], ["test", 1.8, 2.2], ["transcription", 2.2, 2.7] ] } ] } ] } }
Error Response: { "error": "Video URL is required" }
/health
Method: GET
Description: Health check endpoint for monitoring the app's availability.
Response: { "status": "healthy" }
Deployment

Deploy on Render:

Push the repository to GitHub.

Connect the repository to Render and create a new Web Service.

Configure the build and start commands:

Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Use the public URL provided by Render for testing (e.g., https://your-app-name.onrender.com).

Testing

Using Postman:

Create a new POST request to: https://your-app-name.onrender.com/transcribe

Set the request body to raw JSON: { "video_url": "https://example.com/video.mp4", "direct_transcription": true }

Send the request and check the transcription result.

Health Check:

Send a GET request to: https://your-app-name.onrender.com/health
Verify that the app responds with {"status": "healthy"}.
Folder Structure: transcription-api/

app.py # Main application file
requirements.txt # Python dependencies
videos/ # Folder for storing downloaded videos
Future Improvements:

Add support for multiple languages in transcription.
Implement asynchronous processing for large video files.
Cache transcription results for repeated requests.
Add authentication to secure the API.
Contributing: Contributions are welcome! Please fork the repository and create a pull request for any changes or improvements.

License: This project is licensed under the MIT License. See the LICENSE file for more details.

ideo Transcription API

A Python-based Flask API for video transcription using the Deepgram API. This API supports transcribing video files from URLs, including Google Drive links, and provides transcription results in JSON format with word-level timestamps.

Features:

Transcription Options:
Direct Transcription: Transcribe audio directly from a URL.
Local Transcription: Download the video to the server before transcription.
Supports Google Drive Links: Converts Google Drive sharing links into direct download links automatically.
Word-Level Timestamps: Provides detailed transcription results with timestamps for each word.
Health Check Endpoint: A simple /health endpoint for monitoring the app's availability.
Error Handling: Handles invalid URLs, unsupported formats, and other issues gracefully.
Getting Started

Prerequisites:

Python 3.10+
A Deepgram API key (sign up at deepgram.com for an API key)
Installation:

Clone the repository: git clone https://github.com/your-username/transcription-api.git cd transcription-api

Install dependencies: pip install -r requirements.txt

Set up a folder for video downloads: mkdir videos

Add your Deepgram API key: Replace the placeholder DEEPGRAM_API_KEY in app.py with your actual API key.

Usage

Run the API Locally:

Start the Flask app: python app.py

The app will run on: http://127.0.0.1:5000

Endpoints:

/transcribe
Method: POST
Description: Transcribes video files from a URL.
Request Body (JSON): { "video_url": "https://example.com/video.mp4", "direct_transcription": true }
video_url (required): The URL of the video file (supports Google Drive links).
direct_transcription (optional):
true for direct transcription without downloading the video.
false (default) to download the video locally before transcription.
Response (Success): { "results": { "channels": [ { "alternatives": [ { "transcript": "Hello, this is a test transcription.", "timestamps": [ ["Hello", 0.0, 0.5], ["this", 0.5, 1.0], ["is", 1.0, 1.5], ["a", 1.5, 1.8], ["test", 1.8, 2.2], ["transcription", 2.2, 2.7] ] } ] } ] } }
Error Response: { "error": "Video URL is required" }
/health
Method: GET
Description: Health check endpoint for monitoring the app's availability.
Response: { "status": "healthy" }
Deployment

Deploy on Render:

Push the repository to GitHub.

Connect the repository to Render and create a new Web Service.

Configure the build and start commands:

Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
Use the public URL provided by Render for testing (e.g., https://your-app-name.onrender.com).

Testing

Using Postman:

Create a new POST request to: https://your-app-name.onrender.com/transcribe

Set the request body to raw JSON: { "video_url": "https://example.com/video.mp4", "direct_transcription": true }

Send the request and check the transcription result.

Health Check:

Send a GET request to: https://your-app-name.onrender.com/health
Verify that the app responds with {"status": "healthy"}.
Folder Structure: transcription-api/

app.py # Main application file
requirements.txt # Python dependencies
videos/ # Folder for storing downloaded videos
Future Improvements:

Add support for multiple languages in transcription.
Implement asynchronous processing for large video files.
Cache transcription results for repeated requests.
Add authentication to secure the API.
Contributing: Contributions are welcome! Please fork the repository and create a pull request for any changes or improvements.

License: This project is licensed under the MIT License. See the LICENSE file for more details.

