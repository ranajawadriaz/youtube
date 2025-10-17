# FastAPI YouTube Transcript to PDF Service

## Overview
This service accepts a YouTube URL and a prompt, extracts the video transcript, and generates a professionally formatted PDF with text and AI-generated images based on your instructions.

## Features
- 🎥 **YouTube Transcript Extraction**: Downloads and transcribes any YouTube video
- 📄 **Smart PDF Generation**: Creates structured PDFs based on your custom prompt
- 🖼️ **AI-Generated Images**: Adds relevant images to sections using Google Gemini Imagen
- 📦 **ZIP Output**: Returns both transcript (.txt) and PDF in a single ZIP file
- 🧹 **Auto Cleanup**: Automatically removes temporary files after processing

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
The service uses three separate Google Gemini API keys (configured in `enhanced_config.py`):
- **GEMINI_API_KEY**: For transcript cleanup
- **GEMINI_TEXT_API_KEY**: For PDF content generation
- **GEMINI_IMAGE_API_KEY**: For image generation

All keys are already configured.

### 3. Start the Service
```bash
python main_api.py
```

Or with auto-reload for development:
```bash
uvicorn main_api:app --reload --host 0.0.0.0 --port 8000
```

The service will start on `http://localhost:8000`

### 4. Test the Service
```bash
python test_api.py
```

## API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "YouTube Transcript to PDF Generator"
}
```

### Generate Transcript & PDF
```http
POST /generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "prompt": "Your detailed instructions for PDF structure and content..."
}
```

**Response:**
- Content-Type: `application/zip`
- Downloads: `transcript_and_pdf.zip` containing:
  - `extracted_transcript.txt` - Raw transcript
  - `structured.pdf` - Formatted PDF with images

## Prompt Guidelines

The `prompt` field controls how the PDF is structured and what images are generated. Here's an example:

```text
Create a professional document with the following structure:

1. **Introduction**: Brief overview of the video content
2. **Main Topics**: Core concepts discussed (include 2-3 relevant images)
3. **Key Takeaways**: Important points to remember
4. **Detailed Analysis**: In-depth explanation
5. **Conclusion**: Summary and final thoughts

Style guidelines:
- Use clear headings and subheadings
- Include relevant images for visual concepts
- Keep paragraphs concise
- Professional academic tone
- Highlight key terms
```

### Tips for Better Results:
- Be specific about the structure you want
- Mention where you want images (sections, topics)
- Specify tone and style preferences
- Include formatting guidelines
- Request specific types of content (summaries, analyses, etc.)

## How It Works

1. **Transcript Extraction**:
   - Downloads YouTube video audio using yt-dlp
   - Converts to WAV using FFmpeg
   - Transcribes using Google Speech Recognition (free)
   - Cleans up transcript using Gemini API

2. **PDF Generation**:
   - Sends transcript + prompt to Gemini Text API (gemini-2.5-flash)
   - Gets structured JSON with sections and image prompts
   - Generates images using Gemini Imagen API (imagen-4.0-ultra)
   - Creates PDF using ReportLab with custom formatting
   - Applies professional styles (titles, headings, body text)

3. **Delivery**:
   - Packages transcript.txt and structured.pdf into ZIP
   - Returns ZIP file to client
   - Cleans up temporary files in background

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  FastAPI Service                     │
│                   (main_api.py)                      │
└───────────────┬─────────────────────────────────────┘
                │
                ├── POST /generate
                │   ├── Input: {youtube_url, prompt}
                │   └── Output: ZIP file
                │
                ├── YouTubeTranscriptExtractor
                │   ├── yt-dlp (download)
                │   ├── FFmpeg (convert)
                │   ├── SpeechRecognition (transcribe)
                │   └── Gemini API (cleanup)
                │
                └── PDFGenerator (pdf_generator.py)
                    ├── Gemini Text API (structure)
                    ├── Gemini Imagen API (images)
                    └── ReportLab (PDF creation)
```

## Configuration

### API Keys (enhanced_config.py)
```python
GEMINI_API_KEY = "AIzaSyDFqnd7vddPTNZjvSLCXZ2xHyOubHlaKlc"  # Transcript
GEMINI_TEXT_API_KEY = "AIzaSyBAksL_56Q40LbQXn2qgvxlEdiWCXXxoGo"  # Text
GEMINI_IMAGE_API_KEY = "AIzaSyBN7_v_0PO8HXh0i0KOsNHvRxdh2DTLHyc"  # Images
```

### Server Settings
- **Port**: 8000 (default)
- **Host**: 0.0.0.0 (all interfaces)
- **Timeout**: 5 minutes per request
- **Temp Files**: Auto-cleanup enabled

## Example Usage

### Python
```python
import requests

response = requests.post(
    'http://localhost:8000/generate',
    json={
        'youtube_url': 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
        'prompt': 'Create a 5-section document with images for main concepts'
    }
)

with open('result.zip', 'wb') as f:
    f.write(response.content)
```

### cURL
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
    "prompt": "Create a comprehensive guide with visual examples"
  }' \
  --output result.zip
```

### JavaScript
```javascript
const response = await fetch('http://localhost:8000/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    youtube_url: 'https://www.youtube.com/watch?v=jNQXAC9IVRw',
    prompt: 'Create a detailed analysis with supporting images'
  })
});

const blob = await response.blob();
// Download or process the ZIP file
```

## Deployment (Digital Ocean)

### 1. Prepare the Server
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3 python3-pip -y

# Install FFmpeg
sudo apt install ffmpeg -y
```

### 2. Upload Files
```bash
# Create directory
mkdir youtube-pdf-service
cd youtube-pdf-service

# Upload all Python files and requirements.txt
```

### 3. Install Dependencies
```bash
pip3 install -r requirements.txt
```

### 4. Run with Systemd
Create `/etc/systemd/system/youtube-pdf.service`:
```ini
[Unit]
Description=YouTube Transcript to PDF Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/youtube-pdf-service
ExecStart=/usr/bin/python3 -m uvicorn main_api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable youtube-pdf
sudo systemctl start youtube-pdf
sudo systemctl status youtube-pdf
```

### 5. Set Up Nginx (Optional)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 100M;
        proxy_read_timeout 600s;
    }
}
```

## Troubleshooting

### Issue: "FFmpeg not found"
**Solution**: Install FFmpeg or update path in config
```bash
# Linux
sudo apt install ffmpeg

# Windows
# Use included ffmpeg-8.0-essentials_build/bin
```

### Issue: "API Key Invalid"
**Solution**: Verify API keys in `enhanced_config.py` are active

### Issue: "Transcript extraction timeout"
**Solution**: Increase timeout in `youtube_transcript_extractor.py` or use shorter videos

### Issue: "PDF generation fails"
**Solution**: Check prompt format and ensure it's clear and structured

### Issue: "Images not generating"
**Solution**: Verify GEMINI_IMAGE_API_KEY and check API quota

## Performance

- **Average Processing Time**: 2-5 minutes (depends on video length)
- **Max Video Length**: 60 minutes recommended
- **PDF Size**: Typically 2-5 MB with images
- **Concurrent Requests**: Supports multiple simultaneous requests

## Limitations

- YouTube videos must be publicly accessible
- Very long videos (>60 min) may timeout
- Image generation limited by Gemini API quotas
- Requires active internet connection
- Free speech recognition has language limitations

## Future Enhancements

- [ ] Batch processing multiple videos
- [ ] Custom PDF templates
- [ ] Multi-language support
- [ ] Webhook notifications
- [ ] Progress tracking API
- [ ] Caching for repeated URLs
- [ ] Custom image styles

## Support

For issues or questions:
1. Check this README
2. Review `IMPLEMENTATION_SUMMARY.md`
3. Test with `test_api.py`
4. Check service logs

## License

This project uses:
- FFmpeg (GPL/LGPL)
- Google Gemini APIs (Google Terms)
- ReportLab (BSD License)
