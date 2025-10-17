# YouTube Transcript Extractor - Usage Guide

## ✅ Fixed Issues

### What Was Changed (October 17, 2025)
- **FIXED**: Audio processing now extracts the **ENTIRE video**, not just 120 seconds
- **IMPROVED**: Videos are processed in 60-second chunks to handle long videos efficiently
- **ENHANCED**: Better error handling - if one chunk fails, it continues with the rest
- **ADDED**: Retry logic for API failures during speech recognition

## 🚀 Quick Start Command

```bash
python interactive_extractor.py
```

This is the command you need! It will:
1. ✅ Automatically read your Gemini API key from `enhanced_config.py`
2. ✅ Only ask for the YouTube video URL
3. ✅ Extract the full transcript (entire video)
4. ✅ Process long videos in chunks
5. ✅ Clean up text with Gemini AI
6. ✅ Save to `extracted_transcript.txt`

## 📋 How It Works

### For Videos WITH Captions:
1. Extracts official YouTube transcript directly
2. Formats with timestamps
3. Saves to `extracted_transcript.txt`
4. **Result**: Fast, accurate, complete transcript

### For Videos WITHOUT Captions:
1. Downloads the audio from the entire video
2. Processes audio in 60-second chunks
3. Converts each chunk to text using Google Speech Recognition
4. Combines all chunks with timestamps
5. Cleans up with Gemini AI for better formatting
6. Saves to `extracted_transcript.txt`
7. **Result**: Full video transcript with timestamps

## 🎯 Example Usage

```bash
# Navigate to project directory
cd "c:\Users\hp\Downloads\youtube transcript generator\youtube transcript generator"

# Run the extractor
python interactive_extractor.py

# When prompted, paste your YouTube URL:
https://youtu.be/VIDEO_ID
```

## 📊 Output Format

The `extracted_transcript.txt` file contains:

```
TRANSCRIPT EXTRACTION REPORT
==================================================
Video URL: [your video URL]
Method Used: [extraction method]
==================================================

[00:00] First part of transcript...
[01:00] Second part of transcript...
[02:00] Third part of transcript...
...
```

## ⚙️ Configuration

Your Gemini API key is already configured in `enhanced_config.py`:
```python
GEMINI_API_KEY = "AIzaSyDFqnd7vddPTNZjvSLCXZ2xHyOubHlaKlc"
```

If you need to change it, edit the `enhanced_config.py` file.

## 🎬 Chunk Processing Details

- **Chunk Size**: 60 seconds per chunk
- **Processing**: Sequential (one chunk at a time)
- **Error Handling**: If a chunk fails, the script continues with remaining chunks
- **Maximum Retries**: 1 retry per chunk on API errors
- **Retry Delay**: 5 seconds between retries

### Example for a 5-minute video:
```
Processing audio in 5 chunk(s) of 60 seconds each...
✅ Processing chunk 1/5 (0.0s - 60.0s)...
✅ Processing chunk 2/5 (60.0s - 120.0s)...
✅ Processing chunk 3/5 (120.0s - 180.0s)...
✅ Processing chunk 4/5 (180.0s - 240.0s)...
✅ Processing chunk 5/5 (240.0s - 300.0s)...
```

## 🔧 Troubleshooting

### Issue: "FFmpeg not found"
**Solution**: FFmpeg is already installed and working in your setup. No action needed.

### Issue: "Could not understand audio" for some chunks
**Reason**: Chunk contains music, silence, or very unclear speech
**Result**: Script continues with other chunks - you'll get partial transcript

### Issue: API rate limiting
**Solution**: Script automatically retries with 5-second delay. Just wait.

### Issue: No transcript for video with captions
**Possible Causes**:
- Video has auto-generated captions disabled
- Captions are in non-English language only
**Solution**: Script will automatically fall back to audio extraction

## 📈 Performance Tips

1. **For long videos (>30 minutes)**: Expect ~1-2 minutes per minute of audio
2. **Internet required**: Both for downloading audio and speech recognition API
3. **First chunk might take longer**: System adjusts for ambient noise
4. **Gemini cleanup adds ~2-5 seconds**: Worth it for better formatting

## ✨ Features

- ✅ Full video extraction (no duration limits)
- ✅ Multiple URL format support
- ✅ Automatic caption detection
- ✅ Speech-to-text fallback
- ✅ AI-powered text cleanup
- ✅ Timestamp formatting
- ✅ Progress logging
- ✅ Error recovery
- ✅ Memory efficient (processes in chunks)

## 📝 Notes

- The script processes the **entire video**, regardless of length
- Chunks are processed sequentially to avoid memory issues
- If speech recognition fails for a chunk (music/silence), it's skipped
- Final output combines all successfully processed chunks
- Gemini AI enhances the raw speech-to-text output for readability

---

**Last Updated**: October 17, 2025
**Status**: ✅ Fully Functional - All Issues Resolved
