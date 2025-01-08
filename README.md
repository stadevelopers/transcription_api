# Video Transcription API

This project provides a Python-based Flask API for transcribing video files using the Deepgram API. The API can transcribe audio directly from URLs or from videos downloaded locally. It supports Google Drive links and provides transcription results in JSON format with word-level timestamps.

---

## Features
- **Transcription Options:**
  - Direct transcription: Transcribe audio directly from a URL.
  - Local transcription: Download the video locally before transcription.
- **Google Drive Support:** Automatically converts Google Drive sharing links into direct download links.
- **Word-Level Timestamps:** Provides detailed transcription results with timestamps for each word.
- **Health Check Endpoint:** A `/health` endpoint for monitoring the API’s availability.
- **Error Handling:** Handles invalid URLs, unsupported formats, and other issues gracefully.

---

## Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

Ensure you have the following installed:
- Python 3.10 or later
- `pip` (Python package manager)
- A valid Deepgram API key (you can generate one by signing up at [Deepgram’s API portal](https://deepgram.com/)).

---

### 2. Install Dependencies

Clone the repository and install the required Python packages:

```bash
git clone <repository_url>
cd <repository_folder>
pip install -r requirements.txt
```

---

### 3. Configure API Key

The Deepgram API key is part of the code. Follow these steps to set up the Deepgram API key and include it in the project:

#### Steps to Set Up the API Key:
1. Visit the [Deepgram API portal](https://deepgram.com/) and sign up or log in.
2. Navigate to the "API Keys" section in your account dashboard.
3. Generate a new API key.
4. Open the `app.py` file in the project directory.
5. Replace the placeholder in this line with your API key:
   ```python
   DEEPGRAM_API_KEY = 'your_api_key_here'
   ```
6. Save the changes.

---

### 4. Run the Application Locally

Start the Flask application by running:

```bash
python app.py
```

The application will run on `http://127.0.0.1:5000`. You can test the endpoints using tools like [Postman](https://www.postman.com/) or `curl`.

---

## API Endpoints

### `POST /transcribe`

#### Request:
- Accepts a JSON payload with the following fields:
  - `video_url`: (Required) URL of the video file (supports Google Drive links).
  - `direct_transcription`: (Optional) Set to `true` for direct transcription without downloading the video; defaults to `false`.

#### Example (using `curl`):
```bash
curl -X POST -H "Content-Type: application/json" \
    -d '{"video_url": "https://example.com/video.mp4", "direct_transcription": true}' \
    http://127.0.0.1:5000/transcribe
```

#### Response:
- A JSON object containing the transcription and word-level timestamps.

Example Response:
```json
{
  "results": {
    "channels": [
      {
        "alternatives": [
          {
            "transcript": "Hello, this is a test transcription.",
            "timestamps": [
              ["Hello", 0.0, 0.5],
              ["this", 0.5, 1.0],
              ["is", 1.0, 1.5],
              ["a", 1.5, 1.8],
              ["test", 1.8, 2.2],
              ["transcription", 2.2, 2.7]
            ]
          }
        ]
      }
    ]
  }
}
```

#### Error Response:
```json
{
  "error": "Video URL is required"
}
```

---

### `GET /health`

#### Request:
- No parameters required.

#### Response:
```json
{
  "status": "healthy"
}
```

---

## Deployment

Deploy the project on Render or similar platforms by following these steps:

1. Create a private repository on GitHub.
2. Link the GitHub repository to Render during the service setup.
3. Provide the following commands during setup:
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     gunicorn app:app --bind 0.0.0.0:$PORT
     ```
4. Render will provide a public URL for testing (e.g., `https://your-app-name.onrender.com`).

---

## Tools and Technologies Used
- **Flask**: Web framework for building the API.
- **Deepgram API**: For video transcription.
- **Render**: For deployment.
- **Postman**: For testing the endpoints.

---

## Future Improvements
- Add support for multiple languages in transcription.
- Implement asynchronous processing for large video files.
- Cache transcription results for repeated requests.
- Add authentication to secure the API.

---

## Contributing

Contributions are welcome! Please fork the repository and create a pull request for any changes or improvements.

---

