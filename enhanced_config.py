# Enhanced YouTube Transcript Extractor Configuration

# Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyDFqnd7vddPTNZjvSLCXZ2xHyOubHlaKlc"  # For transcript cleanup
GEMINI_TEXT_API_KEY = "AIzaSyBAksL_56Q40LbQXn2qgvxlEdiWCXXxoGo"  # For text generation (gemini_text.py)
GEMINI_IMAGE_API_KEY = "AIzaSyB6_Wja8c0UZYoouayNYC5La4FIiL3NCy4"  # For image generation (gemini_image.py) - NEW KEY with fresh quota!

# Audio Processing Configuration
AUDIO_QUALITY = "192K"  # Audio quality for downloads
AUDIO_FORMAT = "wav"    # Audio format for speech recognition

# Speech Recognition Configuration
SPEECH_RECOGNITION_TIMEOUT = 300  # Timeout in seconds for speech recognition
CHUNK_SIZE = 60  # Size of audio chunks for processing (in seconds)

# Language Preferences for YouTube Transcripts
LANGUAGE_PREFERENCES = [
    ["en"],      # Manual English transcripts
    ["en-US"],   # English US transcripts  
    ["en-GB"],   # English UK transcripts
    ["a.en"],    # Auto-generated English transcripts
]

# File Configuration
DEFAULT_OUTPUT_FILE = "extracted_transcript.txt"
LOG_LEVEL = "INFO"  # Logging level: DEBUG, INFO, WARNING, ERROR

# AI Cleanup Configuration
USE_AI_CLEANUP = True  # Whether to use Gemini API for text cleanup
AI_MODEL = "gemini-2.0-flash-exp"  # Gemini model to use for cleanup

# Retry Configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Note: For the Gemini API cleanup feature to work, you need to:
# 1. Get an API key from Google AI Studio (https://makersuite.google.com/app/apikey)
# 2. Set the GEMINI_API_KEY variable above
# 3. Ensure you have the google-genai package installed