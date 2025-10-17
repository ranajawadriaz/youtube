# Enhanced YouTube Transcript Extractor

A powerful Python tool that extracts transcripts from any YouTube video with intelligent fallback options and AI-powered text cleanup.

## 🌟 Features

### Core Functionality
- **Universal YouTube Support**: Works with any YouTube video URL
- **Multiple URL Formats**: Supports both `youtube.com/watch?v=` and `youtu.be/` formats
- **Direct Transcript Extraction**: Gets official transcripts when available
- **Smart Fallback**: Downloads audio and converts to text when no transcript exists
- **AI Text Cleanup**: Uses Google's Gemini API to clean and structure raw speech-to-text output

### Advanced Capabilities
- **Multi-language Support**: Attempts multiple language preferences
- **Progress Tracking**: Real-time progress updates during processing
- **Error Handling**: Comprehensive error handling with helpful messages
- **Output Flexibility**: Save to file or display in terminal
- **Interactive Interface**: User-friendly command-line interface

## 🚀 Quick Start

### 1. Installation

Run the setup script:
```bash
# Windows
enhanced_setup.bat

# Or manually install dependencies
pip install -r requirements.txt
```

### 2. Basic Usage

#### Interactive Mode (Recommended for beginners)
```bash
python interactive_extractor.py
```

#### Command Line Mode
```bash
# Basic usage
python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=VIDEO_ID"

# With Gemini API for text cleanup
python youtube_transcript_extractor.py "https://youtu.be/VIDEO_ID" "YOUR_GEMINI_API_KEY"
```

## 📋 Supported URL Formats

The tool automatically detects and processes these YouTube URL formats:

```
https://www.youtube.com/watch?v=bzZjG9B9_Ug
https://youtu.be/bzZjG9B9_Ug
https://youtu.be/bzZjG9B9_Ug?si=mC4gd1LMv0ba85tv
```

## 🔧 Configuration

### Gemini API Setup (Optional but Recommended)

1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add it to `enhanced_config.py`:
   ```python
   GEMINI_API_KEY = "your_api_key_here"
   ```
3. Or provide it when prompted in interactive mode

### Other Configuration Options

Edit `enhanced_config.py` to customize:
- Audio quality settings
- Language preferences
- Output file locations
- AI model selection

## 🔄 How It Works

### Step 1: Direct Transcript Extraction
- Attempts to get official YouTube transcripts
- Tries multiple language preferences
- Returns formatted transcript with timestamps

### Step 2: Audio Fallback (if no transcript)
- Downloads video audio using yt-dlp
- Converts audio to text using Google Speech Recognition
- Processes audio in optimized chunks for better accuracy

### Step 3: AI Enhancement (optional)
- Sends raw speech-to-text to Gemini API
- Cleans up transcription errors
- Adds proper formatting and structure
- Maintains original meaning while improving readability

## 📦 Dependencies

### Core Dependencies
- `youtube-transcript-api` - Direct transcript extraction
- `yt-dlp` - Video/audio downloading
- `SpeechRecognition` - Speech-to-text conversion
- `pydub` - Audio processing
- `google-genai` - AI text cleanup

### System Requirements
- Python 3.8+
- FFmpeg (for audio processing)
- Internet connection

### Installing FFmpeg

#### Windows
```bash
# Using Chocolatey
choco install ffmpeg

# Using Scoop
scoop install ffmpeg

# Manual: Download from https://ffmpeg.org/download.html
```

#### macOS
```bash
brew install ffmpeg
```

#### Linux
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # CentOS/RHEL
```

## 💡 Usage Examples

### Example 1: Basic Extraction
```bash
python youtube_transcript_extractor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Example 2: With AI Cleanup
```bash
python youtube_transcript_extractor.py "https://youtu.be/dQw4w9WgXcQ" "your_gemini_api_key"
```

### Example 3: Interactive Mode
```bash
python interactive_extractor.py
# Follow the prompts to enter URL and API key
```

## 📄 Output Format

The tool generates well-formatted transcripts with:
- Timestamps in [MM:SS] or [HH:MM:SS] format
- Proper text formatting
- Source information (method used, video URL)
- Processing details

Example output:
```
TRANSCRIPT EXTRACTED USING: YOUTUBE_TRANSCRIPT
VIDEO URL: https://www.youtube.com/watch?v=VIDEO_ID
================================================================================
[00:00] Welcome to this video about amazing topics
[00:15] In today's session we'll cover several important points
[00:30] First, let's discuss the main concept...
```

## 🐛 Troubleshooting

### Common Issues

#### "FFmpeg not found"
- Install FFmpeg using instructions above
- Ensure FFmpeg is in your system PATH

#### "No transcript available" + Audio processing fails
- Video might be private or age-restricted
- Audio quality might be too poor for recognition
- Try a different video to test the tool

#### "Rate limiting" errors
- YouTube has API limits; wait a few minutes and try again
- Use the tool moderately to avoid hitting limits

#### Gemini API errors
- Check your API key is correct
- Ensure you have API credits available
- Verify internet connection

### Getting Help

1. Check the error message for specific guidance
2. Ensure all dependencies are installed correctly
3. Try the interactive mode for better error reporting
4. Test with a known working video URL

## 📈 Advanced Features

### Batch Processing
While not included in the basic version, you can easily extend the tool for batch processing:

```python
from youtube_transcript_extractor import YouTubeTranscriptExtractor

urls = ["url1", "url2", "url3"]
extractor = YouTubeTranscriptExtractor("your_api_key")

for url in urls:
    transcript, method = extractor.extract_transcript(url)
    # Process each transcript
```

### Custom Audio Processing
The tool uses high-quality audio settings by default, but you can customize:
- Audio quality (192K default)
- Chunk size for processing
- Recognition timeout settings

## 🔒 Privacy & Security

- No data is stored permanently (except your chosen output files)
- Audio files are processed in temporary directories and deleted
- API keys should be kept secure and not shared
- The tool only accesses public YouTube videos

## 📝 Migration from Netflix Version

If you're upgrading from the Netflix-specific version:

1. **Backup your old configuration**
2. **Install new dependencies**: `pip install -r requirements.txt`
3. **Update your scripts**: Use new file names
4. **Configure Gemini API**: Add API key for enhanced features

The old Netflix-specific files (`main.py`, `config.py`) are preserved but the new enhanced version provides much more flexibility.

## 🤝 Contributing

Feel free to contribute improvements:
- Support for additional video platforms
- Better audio processing algorithms
- Enhanced AI prompting for cleanup
- Additional output formats

## 📄 License

This project is provided as-is for educational and personal use. Respect YouTube's terms of service and content creators' rights when using this tool.