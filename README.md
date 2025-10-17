# Enhanced YouTube Transcript Extractor# Enhanced YouTube Transcript Extractor (JavaScript/Node.js)# Enhanced YouTube Transcript Extractor# Netflix YouTube Transcript Extractor



A powerful Python tool that extracts transcripts from any YouTube video with intelligent fallback options and AI-powered text cleanup.



## ✨ FeaturesA powerful Node.js tool that extracts transcripts from any YouTube video with intelligent fallback options and AI-powered text cleanup.



- **Universal YouTube Support**: Works with any YouTube video URL

- **Automatic Transcript Extraction**: Gets official transcripts when available

- **FREE Speech-to-Text Fallback**: Downloads audio and converts to text when no transcript exists## ✨ FeaturesA powerful Python tool that extracts transcripts from any YouTube video with intelligent fallback options and AI-powered text cleanup.This Python tool automatically extracts transcript text from the latest videos uploaded to Netflix's official YouTube channel (https://www.youtube.com/@Netflix/videos). The script is designed to run every hour and capture transcripts from videos uploaded in the past hour.

- **AI Text Cleanup**: Uses Google's Gemini API to clean and format raw transcriptions

- **Complete Metadata Extraction**: Saves video title, channel, views, likes, description, tags, and more

- **Full Video Processing**: No duration limits - processes entire videos

- **Intelligent Chunking**: Breaks long videos into 30-second chunks for optimal processing- **Universal YouTube Support**: Works with any YouTube video URL

- **Error Recovery**: Continues processing even if some chunks fail

- **Automatic Transcript Extraction**: Gets official transcripts when available

## 🚀 Quick Start

- **Speech-to-Text Fallback**: Downloads audio and converts to text when no transcript exists## ✨ Features## Features

### Prerequisites

- **AI Text Cleanup**: Uses Google's Gemini API to clean and format raw transcriptions

- **Python 3.8+**: Already installed

- **FFmpeg**: Already included in `ffmpeg-8.0-essentials_build/`- **Complete Metadata Extraction**: Saves video title, channel, views, likes, description, tags, and more



### Installation- **Full Video Processing**: No duration limits - processes entire videos



**Install Python dependencies**:- **Intelligent Chunking**: Breaks long videos into 30-second chunks for optimal processing- **Universal YouTube Support**: Works with any YouTube video URL- **Automatic transcript extraction** from Netflix's YouTube channel

```bash

pip install -r requirements.txt- **Error Recovery**: Continues processing even if some chunks fail

```

- **Automatic Transcript Extraction**: Gets official transcripts when available- **Multiple language support** including auto-generated English transcripts

### Configuration (Optional)

## 🚀 Quick Start

**Gemini API** (for AI text cleanup):

- Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)- **Speech-to-Text Fallback**: Downloads audio and converts to text when no transcript exists- **Rate limiting protection** to avoid YouTube API blocks

- Edit `enhanced_config.py` and add your API key

### Prerequisites

### Usage

- **AI Text Cleanup**: Uses Google's Gemini API to clean and format raw transcriptions- **Formatted output** with timestamps and video information

**Interactive Mode** (recommended):

```bash- **Node.js 18+**: Download from [nodejs.org](https://nodejs.org/)

python interactive_extractor.py

```- **FFmpeg**: Required for audio processing (see installation below)- **Complete Metadata Extraction**: Saves video title, channel, views, likes, description, tags, and more- **Error handling** for videos without transcripts or with disabled transcripts

Then paste any YouTube URL when prompted!



**Command Line Mode**:

```bash### Installation- **Full Video Processing**: No duration limits - processes entire videos- **Test mode** for checking videos from the past 24 hours

python youtube_transcript_extractor.py "https://youtube.com/watch?v=VIDEO_ID"

```



## 📋 Supported URL Formats1. **Install Node.js dependencies**:- **Intelligent Chunking**: Breaks long videos into 30-second chunks for optimal processing



- `https://www.youtube.com/watch?v=VIDEO_ID`   ```bash

- `https://youtu.be/VIDEO_ID`

- `https://youtu.be/VIDEO_ID?si=SHARE_ID`   npm install- **Error Recovery**: Continues processing even if some chunks fail## Files Structure



## 📝 Output   ```



Results are saved to `extracted_transcript.txt` with complete video metadata and formatted transcript including:

- Video title, channel, duration, views, likes

- Full description, tags, and categories2. **Install FFmpeg** (Windows):

- Extraction method used

- Timestamped transcript text   ```bash## 🚀 Quick Start```



## ⚙️ Configuration   choco install ffmpeg



Edit `enhanced_config.py` to customize:   # ornetflix-transcript-extractor/

- **GEMINI_API_KEY**: Your Gemini API key for AI cleanup

- **AUDIO_QUALITY**: Audio download quality (default: "192K")   scoop install ffmpeg

- **CHUNK_SIZE**: Audio chunk size in seconds (default: 60)

- **AI_MODEL**: Gemini model to use (default: "gemini-2.0-flash-exp")   # or### Installation├── main.py                           # Main Python script

- **LANGUAGE_PREFERENCES**: Transcript language priorities

   winget install ffmpeg

## 📦 Requirements

   ```├── config.py                         # Configuration settings

- **Python**: 3.8 or higher

- **FFmpeg**: For audio processing (included locally)   

- **Internet connection**: For downloading videos and API calls

   Or use the local FFmpeg installation already included in `ffmpeg-8.0-essentials_build/`1. **Install Python dependencies**:├── transcript.txt                    # Output file containing extracted transcripts

### Python Dependencies



All in `requirements.txt`:

- `youtube-transcript-api` - YouTube transcript extraction3. **Configure Gemini API** (optional but recommended):   ```bash├── run_hourly.bat                    # Windows batch script for hourly execution

- `yt-dlp` - YouTube video downloading

- `SpeechRecognition` - FREE Google Speech Recognition   - Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

- `pydub` - Audio processing

- `google-genai` - Gemini AI integration   - Edit `config.js` and add your API key   enhanced_setup.bat├── run_hourly.ps1                    # PowerShell script for hourly execution

- `requests` - HTTP requests

- `ffmpeg-python` - FFmpeg wrapper



## 🔧 How It Works### Usage   ```├── netflix_transcript_hourly_task.xml # Windows Task Scheduler template



1. **Transcript Extraction**: First tries to get official YouTube transcripts

2. **Audio Fallback**: If no transcript, downloads audio using `yt-dlp`

3. **Speech Recognition**: Converts audio to text using FREE Google Speech Recognition**Interactive Mode** (recommended):├── requirements.txt                  # Python package requirements

4. **AI Cleanup**: Cleans up raw text with Gemini API (optional)

5. **Metadata Extraction**: Gets all video information```bash

6. **Formatted Output**: Saves everything to `extracted_transcript.txt`

npm start2. **Configure Gemini API** (optional but recommended):├── test_extractor.py                 # Test script for verification

## 🎯 Examples

# or

### Example 1: Video with Transcript

```bashnode interactiveExtractor.js   - Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)└── README.md                        # This documentation file

python interactive_extractor.py

# Enter: https://www.youtube.com/watch?v=dQw4w9WgXcQ```

# Result: Instant transcript extraction

```Then paste any YouTube URL when prompted!   - Edit `enhanced_config.py` and add your API key```



### Example 2: Video without Transcript

```bash

python interactive_extractor.py**Command Line Mode**:

# Enter: https://youtu.be/rFGiHm5WMLk

# Result: Downloads audio → Speech recognition → AI cleanup```bash

```

node youtubeTranscriptExtractor.js "https://youtube.com/watch?v=VIDEO_ID"### Usage## Installation

## 🐛 Troubleshooting

# or with Gemini API key

### FFmpeg not found

The tool checks for FFmpeg in:node youtubeTranscriptExtractor.js "https://youtube.com/watch?v=VIDEO_ID" "YOUR_API_KEY"

1. Local directory: `ffmpeg-8.0-essentials_build/bin/`

2. System PATH```



FFmpeg is already included, so this should work automatically!Simply run:1. **Python Environment**: The script uses a virtual environment located at `D:/youtube transcript generator/.venv/`



### Short/Incomplete Transcripts## 📋 Supported URL Formats

Normal for videos with lots of music or silence. The tool:

- Processes all audio chunks```bash

- Shows which chunks succeeded/failed

- Extracts all recognizable speech- `https://www.youtube.com/watch?v=VIDEO_ID`



### No Transcript Available- `https://youtu.be/VIDEO_ID`python interactive_extractor.py2. **Required packages** (automatically installed):

If a video has no official transcript:

- Tool automatically downloads audio ✅- `https://youtu.be/VIDEO_ID?si=SHARE_ID`

- Converts to text using FREE Google Speech Recognition ✅

- Cleans up with Gemini AI ✅```   - `scrapetube` - For fetching YouTube channel videos



## 💡 Tips## 📝 Output



- **Most videos** (90%+) have official transcripts and work instantly   - `youtube-transcript-api` - For extracting video transcripts

- **Videos without transcripts** are processed automatically with speech recognition (FREE!)

- **Music videos** may have limited transcription (mostly lyrics when audible)Results are saved to `extracted_transcript.txt` with complete video metadata and formatted transcript including:

- **Educational videos** usually have excellent transcripts

- **Trailers** may have limited speech (lots of music/sound effects)- Video title, channel, duration, views, likesThen paste any YouTube URL when prompted!   - `requests` - For HTTP requests



## 📄 Project Structure- Full description, tags, and categories



```- Extraction method used   - `beautifulsoup4` - For HTML parsing (backup functionality)

youtube-transcript-extractor/

├── youtube_transcript_extractor.py  # Main extractor class- Timestamped transcript text

├── interactive_extractor.py         # Interactive CLI interface

├── enhanced_config.py               # Configuration settings## 📋 Supported URL Formats

├── ffmpeg_helper.py                 # FFmpeg detection utilities

├── requirements.txt                 # Python dependencies## ⚙️ Configuration

├── extracted_transcript.txt         # Output file (generated)

├── ffmpeg-8.0-essentials_build/     # Local FFmpeg installation## Usage

└── README.md                        # This file

```Edit `config.js` to customize:



## 🎓 Features in Detail- **GEMINI_API_KEY**: Your Gemini API key for AI cleanup- `https://www.youtube.com/watch?v=VIDEO_ID`



### Free Speech Recognition- **AUDIO_QUALITY**: Audio download quality (default: "192K")

Uses Python's `SpeechRecognition` library with Google's free speech API:

- No API key required- **CHUNK_SIZE**: Audio chunk size in seconds (default: 60)- `https://youtu.be/VIDEO_ID`### Running the Script

- No authentication needed

- Completely free- **AI_MODEL**: Gemini model to use (default: "gemini-2.0-flash-exp")

- Same quality as paid APIs for most content

- **DEFAULT_OUTPUT_FILE**: Output filename (default: "extracted_transcript.txt")- `https://youtu.be/VIDEO_ID?si=SHARE_ID`

### Gemini AI Cleanup

Optional feature that:

- Adds proper punctuation

- Fixes capitalization## 📦 Requirements**Normal Mode (Check last 1 hour):**

- Breaks into paragraphs

- Corrects transcription errors

- Makes text more readable

- **Node.js**: 18.0.0 or higher## 📝 Output```bash

### Intelligent Chunking

Processes long videos efficiently:- **FFmpeg**: For audio processing (automatically detected in local directory or system PATH)

- Splits audio into 30-second chunks

- Processes each chunk independently- **Internet connection**: For downloading videos and API callspython main.py

- Continues even if some chunks fail

- Combines all successful chunks



## 📄 License### Node.js DependenciesResults are saved to `extracted_transcript.txt` with complete video metadata and formatted transcript.```



For educational and personal use. Respect YouTube's terms of service and rate limits.



---All dependencies are listed in `package.json`:



**Version**: 2.0 - Clean and optimized  - `@google/generative-ai` - Gemini AI integration

**Language**: Python 3.8+  

**Status**: Production Ready ✅- `youtube-transcript` - Direct transcript extraction## ⚙️ Configuration**Test Mode (Check last 24 hours):**


- `@distube/ytdl-core` - YouTube video downloading

- `fluent-ffmpeg` - FFmpeg wrapper for audio processing```bash

- `readline-sync` - Interactive CLI prompts

- `chalk` - Terminal styling (optional)Edit `enhanced_config.py` to customize:python main.py --test



## 🔧 Troubleshooting- Gemini API key```



### FFmpeg not found- Audio quality settings

The tool automatically checks for FFmpeg in:

1. Local directory: `ffmpeg-8.0-essentials_build/bin/`- Language preferences**Help:**

2. System PATH

- Chunk size```bash

If not found, install with:

```bashpython main.py --help

choco install ffmpeg

```## 📦 Requirements```



### Speech-to-Text Limitations

**Important Note**: The JavaScript version includes audio extraction but requires Google Cloud Speech-to-Text API integration for actual transcription. The Python version has this fully implemented with Google Speech Recognition.

- Python 3.8+### Automatic Hourly Execution

To fully implement speech-to-text:

1. Set up Google Cloud Speech-to-Text API- FFmpeg (install with `install_ffmpeg.bat`)

2. Integrate the API in `youtubeTranscriptExtractor.js` in the `audioToText()` method

3. Or use another speech recognition service- Internet connection**Option 1: Using Batch File**



### Short/Incomplete Transcripts```bash

Normal for videos with lots of music or silence. The tool extracts all recognizable speech and continues even if some chunks fail.

## 🔧 Troubleshootingrun_hourly.bat

### No Transcript Available

If a video has no official transcript and speech-to-text fails:```

- Try a different video

- Check if the video has captions enabled on YouTube### FFmpeg not found

- Ensure FFmpeg is installed and working

```bash**Option 2: Using PowerShell**

## 🆚 Python vs JavaScript Version

install_ffmpeg.bat```powershell

**Python Version** (original):

- ✅ Fully implemented speech-to-text with Google Speech Recognition```.\run_hourly.ps1

- ✅ Complete audio-to-text conversion without external APIs

- ✅ Works out of the box for videos without transcripts```



**JavaScript Version** (this):### Short transcripts

- ✅ Full transcript extraction from YouTube

- ✅ Complete metadata extractionNormal for videos with lots of music or silence. The tool extracts all recognizable speech.**Option 3: Windows Task Scheduler**

- ✅ Gemini AI text cleanup

- ✅ Audio download and chunkingSet up a Windows Task Scheduler task to run one of the above scripts every hour.

- ⚠️  Speech-to-text requires Google Cloud API integration (not included)

## 📄 License

**Recommendation**: Use the Python version if you need speech-to-text for videos without transcripts. Use the JavaScript version if you only need transcript extraction from videos that already have captions.

**Easy Setup with XML Template:**

## 📄 Project Structure

For educational and personal use. Respect YouTube's terms of service.1. Open Task Scheduler (search "Task Scheduler" in Windows)

```

youtube-transcript-extractor/2. Click "Import Task..." in the right panel

├── config.js                      # Configuration settings

├── youtubeTranscriptExtractor.js  # Main extractor class---3. Select the file `netflix_transcript_hourly_task.xml`

├── interactiveExtractor.js        # Interactive CLI interface

├── ffmpegHelper.js                # FFmpeg detection and helpers4. Modify the task settings if needed (user account, timing, etc.)

├── package.json                   # Node.js dependencies

├── extracted_transcript.txt       # Output file (generated)**Version**: 2.0 - Clean and optimized5. Save the task

├── ffmpeg-8.0-essentials_build/   # Local FFmpeg installation

└── README.md                      # This file

```**Manual Setup:**

1. Open Task Scheduler

## 📄 License2. Create Basic Task

3. Set trigger to "Daily" and repeat every 1 hour

For educational and personal use. Respect YouTube's terms of service and rate limits.4. Set action to "Start a program"

5. Program: `powershell.exe`

---6. Arguments: `-ExecutionPolicy Bypass -File "d:\youtube transcript generator\run_hourly.ps1"`



**Version**: 2.0.0 - JavaScript/Node.js Edition## How It Works



**Converted from**: Python version of Enhanced YouTube Transcript Extractor1. **Video Discovery**: Uses `scrapetube` to fetch the latest videos from Netflix's YouTube channel

2. **Transcript Extraction**: For each video, attempts to extract transcripts using multiple strategies:

**Note**: For full speech-to-text functionality, use the Python version or integrate Google Cloud Speech-to-Text API.   - Manual English transcripts (`en`, `en-US`, `en-GB`)

   - Auto-generated English transcripts (`a.en`)
   - Any available language transcripts
3. **Rate Limiting**: Includes delays between requests to avoid YouTube rate limiting
4. **Output Formatting**: Saves formatted transcripts to `transcript.txt` with:
   - Video title and URL
   - Language and generation type
   - Extraction timestamp
   - Timestamped transcript text

## Output Format

Each transcript in `transcript.txt` follows this format:

```
TRANSCRIPT FOR: Video Title | Netflix
VIDEO URL: https://www.youtube.com/watch?v=VIDEO_ID
LANGUAGE: en-US
IS GENERATED: False
EXTRACTED ON: 2025-09-03 01:16:31
--------------------------------------------------------------------------------

[00:00] First line of transcript
[00:02] Second line of transcript
...


TRANSCRIPT FOR: Next Video Title | Netflix
...
```

Multiple transcripts are separated by two blank lines.

## Error Handling

The script handles various scenarios:

- **No Transcripts Available**: Videos without any transcripts are skipped with a warning
- **Transcripts Disabled**: Videos with disabled transcripts are skipped with a warning
- **Rate Limiting**: Automatic delays and retry logic for YouTube API rate limits
- **Video Unavailable**: Handles unavailable or private videos gracefully

## Limitations

- **YouTube Rate Limits**: YouTube may block requests after multiple consecutive calls
- **Transcript Availability**: Not all videos have transcripts (especially short trailers)
- **Channel Focus**: Currently configured only for Netflix's official channel
- **Language Priority**: Prioritizes English transcripts but can extract others if available

## Troubleshooting

**Common Issues:**

1. **"No transcript found" warnings**: This is normal for videos without transcripts (trailers often don't have them)

2. **Rate limiting errors**: The script includes built-in delays, but if you see rate limiting warnings, the script will automatically handle them

3. **Empty transcript.txt**: This happens when no videos in the time range have available transcripts

4. **Import errors**: Ensure the virtual environment is activated and packages are installed

## Customization

To modify the script for other YouTube channels:

1. Change the `channel_id` and `channel_url` in the `NetflixYouTubeTranscriptExtractor` class
2. Adjust the time range by modifying the `hours_back` parameter
3. Modify language preferences in the `extract_transcript` method

### Configuration File

You can customize the script behavior by editing `config.py`:

- **Channel Settings**: Change `NETFLIX_CHANNEL_ID` and `NETFLIX_CHANNEL_URL`
- **Timing**: Adjust `DEFAULT_TIME_RANGE` and `TEST_TIME_RANGE`
- **Rate Limiting**: Modify `REQUEST_DELAY` and `RETRY_DELAY`
- **Language Preferences**: Update `LANGUAGE_PREFERENCES` list
- **Logging**: Change `LOG_LEVEL` for more or less verbose output
- **Video Limit**: Adjust `MAX_VIDEOS_TO_CHECK`

## Scheduling

For production use, set up the script to run hourly using:

- **Windows Task Scheduler**: Create a task that runs `run_hourly.bat` every hour
- **Cron (if using WSL)**: Add a cron job to run the Python script
- **System Service**: Create a Windows service for continuous operation

## License

This tool is for educational and personal use. Please respect YouTube's Terms of Service and rate limits.
