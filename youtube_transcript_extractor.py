#!/usr/bin/env python3
"""
Enhanced YouTube Transcript Extractor
Extracts transcripts from any YouTube video with fallback to speech-to-text and AI cleanup
"""

import os
import re
import sys
import tempfile
import logging
import random
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs

# Third-party imports
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import speech_recognition as sr
from pydub import AudioSegment
from google import genai
from google.genai import types

# Local imports
from ffmpeg_helper import check_ffmpeg_installation, get_ffmpeg_install_instructions

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class YouTubeTranscriptExtractor:
    def __init__(self, gemini_api_key: Optional[str] = None, use_proxy: bool = False, proxy_list: list = None):
        """
        Initialize the YouTube Transcript Extractor
        
        Args:
            gemini_api_key: API key for Gemini API (optional, for cleanup feature)
            use_proxy: Whether to use proxy rotation (default: False)
            proxy_list: List of proxy URLs to rotate through
        """
        self.gemini_api_key = gemini_api_key
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.current_proxy_index = 0
        self.recognizer = sr.Recognizer()
        
        # Check FFmpeg availability
        self.ffmpeg_available, self.ffmpeg_error = check_ffmpeg_installation()
        if not self.ffmpeg_available:
            logger.warning(f"FFmpeg not available: {self.ffmpeg_error}")
            logger.warning("Speech-to-text fallback will not work without FFmpeg")
    
    def get_next_proxy(self) -> Optional[str]:
        """Get next proxy from the rotation list"""
        if not self.use_proxy or not self.proxy_list:
            return None
        
        proxy = self.proxy_list[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxy_list)
        return proxy
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL
        
        Supports formats:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://youtu.be/VIDEO_ID?si=SHARE_ID
        
        Args:
            url: YouTube video URL
            
        Returns:
            Video ID if valid URL, None otherwise
        """
        # Regex patterns for different YouTube URL formats
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
            r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Alternative method using urlparse for more complex URLs
        try:
            parsed_url = urlparse(url)
            
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                if parsed_url.path == '/watch':
                    query_params = parse_qs(parsed_url.query)
                    if 'v' in query_params:
                        return query_params['v'][0]
            elif parsed_url.hostname in ['youtu.be']:
                # Remove leading slash and any query parameters
                video_id = parsed_url.path.lstrip('/')
                if len(video_id) == 11:  # YouTube video IDs are 11 characters
                    return video_id
        except Exception as e:
            logger.error(f"Error parsing URL: {e}")
        
        return None
    
    def get_video_metadata(self, video_id: str) -> dict:
        """
        Extract metadata from YouTube video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Dictionary containing video metadata
        """
        try:
            logger.info("Fetching video metadata...")
            
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'socket_timeout': 15,
                'retries': 2,
            }
            
            # Add proxy if enabled
            proxy = self.get_next_proxy()
            if proxy:
                ydl_opts['proxy'] = proxy
                logger.info(f"Using proxy: {proxy}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                metadata = {
                    'title': info.get('title', 'N/A'),
                    'channel': info.get('uploader', 'N/A'),
                    'channel_id': info.get('channel_id', 'N/A'),
                    'duration': info.get('duration', 0),
                    'duration_string': info.get('duration_string', 'N/A'),
                    'upload_date': info.get('upload_date', 'N/A'),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'description': info.get('description', 'N/A'),
                    'tags': info.get('tags', []),
                    'categories': info.get('categories', []),
                    'thumbnail': info.get('thumbnail', 'N/A'),
                }
                
                logger.info(f"Metadata fetched: {metadata['title']}")
                return metadata
                
        except Exception as e:
            logger.error(f"Error fetching metadata: {e}")
            return {
                'title': 'N/A',
                'channel': 'N/A',
                'channel_id': 'N/A',
                'duration': 0,
                'duration_string': 'N/A',
                'upload_date': 'N/A',
                'view_count': 0,
                'like_count': 0,
                'description': 'N/A',
                'tags': [],
                'categories': [],
                'thumbnail': 'N/A',
            }
    
    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """
        Extract transcript directly from YouTube video
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Formatted transcript string if available, None otherwise
        """
        try:
            logger.info(f"Attempting to extract transcript for video ID: {video_id}")
            
            # Language preferences (in order of preference)
            language_options = [
                ["en"],      # Manual English transcripts
                ["en-US"],   # English US transcripts
                ["en-GB"],   # English UK transcripts
                ["a.en"],    # Auto-generated English transcripts
            ]
            
            fetched_transcript = None
            
            # Prepare proxies dict for youtube-transcript-api
            proxies = None
            if self.use_proxy and self.proxy_list:
                proxy_url = self.get_next_proxy()
                if proxy_url:
                    proxies = {
                        'http': proxy_url,
                        'https': proxy_url,
                    }
                    logger.info(f"Using proxy for transcript: {proxy_url}")
            
            # Try different language preferences
            for languages in language_options:
                try:
                    fetched_transcript = YouTubeTranscriptApi.get_transcript(
                        video_id, 
                        languages=languages,
                        proxies=proxies
                    )
                    logger.info(f"Found transcript in language preference: {languages}")
                    break
                except (NoTranscriptFound, TranscriptsDisabled):
                    continue
            
            # If no preferred language, try any available transcript
            if fetched_transcript is None:
                try:
                    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id, proxies=proxies)
                    for transcript in transcript_list:
                        try:
                            fetched_transcript = transcript.fetch()
                            logger.info(f"Found transcript in language: {transcript.language_code}")
                            break
                        except:
                            continue
                except:
                    pass
            
            if fetched_transcript is None:
                logger.info("No transcript available for this video")
                return None
            
            # Get raw transcript data
            if hasattr(fetched_transcript, 'to_raw_data'):
                transcript_data = fetched_transcript.to_raw_data()
            else:
                transcript_data = fetched_transcript
            
            # Format the transcript
            formatted_transcript = []
            for entry in transcript_data:
                timestamp = self._format_timestamp(entry['start'])
                text = entry['text'].strip()
                formatted_transcript.append(f"[{timestamp}] {text}")
            
            return "\n".join(formatted_transcript)
            
        except TranscriptsDisabled:
            logger.info("Transcripts are disabled for this video")
            return None
        except NoTranscriptFound:
            logger.info("No transcript found for this video")
            return None
        except VideoUnavailable:
            logger.warning("Video is unavailable")
            return None
        except Exception as e:
            logger.error(f"Error extracting transcript: {e}")
            return None
    
    def download_audio(self, video_id: str, output_path: str) -> bool:
        """
        Download audio from YouTube video
        
        Args:
            video_id: YouTube video ID
            output_path: Path to save the audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Downloading audio from video...")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'extractaudio': True,
                'audioformat': 'wav',
                'audioquality': '192K',
                'quiet': True,
                'no_warnings': True,
                'socket_timeout': 15,
                'retries': 2,
            }
            
            # Add proxy if enabled
            proxy = self.get_next_proxy()
            if proxy:
                ydl_opts['proxy'] = proxy
                logger.info(f"Using proxy: {proxy}")
            
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            logger.info("Audio download completed")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return False
    
    def audio_to_text(self, audio_path: str) -> Optional[str]:
        """
        Convert audio file to text using speech recognition
        Processes the entire audio in chunks to handle long videos
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcribed text if successful, None otherwise
        """
        # Check if FFmpeg is available before attempting audio processing
        if not self.ffmpeg_available:
            logger.error("Cannot process audio: FFmpeg is not installed")
            logger.error(f"FFmpeg error: {self.ffmpeg_error}")
            logger.info("Please install FFmpeg to enable speech-to-text functionality")
            return None
        
        try:
            logger.info("Converting audio to text...")
            
            # Check if audio file exists
            if not os.path.exists(audio_path):
                logger.error(f"Audio file not found: {audio_path}")
                return None
            
            # Log file info for debugging
            file_size = os.path.getsize(audio_path)
            logger.info(f"Processing audio file: {audio_path} (size: {file_size} bytes)")
            
            # Load audio file
            try:
                logger.info("Loading audio file...")
                audio = AudioSegment.from_file(audio_path)
                audio_duration_seconds = len(audio) / 1000  # Convert milliseconds to seconds
                logger.info(f"Audio loaded successfully: {audio_duration_seconds:.1f}s duration")
            except Exception as e:
                logger.error(f"Failed to load audio file with pydub: {e}")
                logger.info("This usually means FFmpeg is not properly installed or accessible")
                return None
            
            # Convert to WAV format with proper settings for speech recognition
            logger.info("Converting audio format for speech recognition...")
            audio = audio.set_frame_rate(16000).set_channels(1)
            
            # Normalize audio to improve recognition
            audio = audio.normalize()
            
            # Process audio in smaller chunks for better API compatibility
            chunk_length_ms = 30000  # 30 seconds per chunk (better for Google API)
            total_chunks = (len(audio) + chunk_length_ms - 1) // chunk_length_ms  # Ceiling division
            
            logger.info(f"Processing audio in {total_chunks} chunk(s) of 30 seconds each...")
            
            all_transcripts = []
            failed_chunks = 0
            
            for chunk_index in range(total_chunks):
                start_ms = chunk_index * chunk_length_ms
                end_ms = min(start_ms + chunk_length_ms, len(audio))
                
                chunk_start_time = start_ms / 1000
                chunk_end_time = end_ms / 1000
                
                logger.info(f"Processing chunk {chunk_index + 1}/{total_chunks} ({chunk_start_time:.1f}s - {chunk_end_time:.1f}s)...")
                
                # Extract chunk
                audio_chunk = audio[start_ms:end_ms]
                
                # Apply noise reduction and normalization to the chunk
                audio_chunk = audio_chunk.normalize()
                
                # Save chunk as temporary WAV file
                temp_wav_path = None
                try:
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
                        temp_wav_path = temp_wav.name
                    
                    audio_chunk.export(temp_wav_path, format="wav")
                    
                    # Process the chunk with speech recognition
                    try:
                        with sr.AudioFile(temp_wav_path) as source:
                            # Adjust for ambient noise with shorter duration
                            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                            
                            # Record the audio data
                            audio_data = self.recognizer.record(source)
                            
                            # Use Google Speech Recognition
                            try:
                                text = self.recognizer.recognize_google(audio_data, language='en-US')
                                
                                # Add timestamp and text
                                timestamp = self._format_timestamp(chunk_start_time)
                                all_transcripts.append(f"[{timestamp}] {text}")
                                logger.info(f"Chunk {chunk_index + 1}/{total_chunks} processed successfully")
                                
                            except sr.UnknownValueError:
                                failed_chunks += 1
                                logger.warning(f"Chunk {chunk_index + 1}/{total_chunks}: Could not understand audio (possibly music, silence, or unclear speech)")
                                # Continue to next chunk instead of failing completely
                                continue
                            except sr.RequestError as e:
                                logger.error(f"API error on chunk {chunk_index + 1}: {e}")
                                logger.info("Waiting 5 seconds before retrying...")
                                import time
                                time.sleep(5)
                                # Try one more time
                                try:
                                    text = self.recognizer.recognize_google(audio_data, language='en-US')
                                    timestamp = self._format_timestamp(chunk_start_time)
                                    all_transcripts.append(f"[{timestamp}] {text}")
                                    logger.info(f"Chunk {chunk_index + 1}/{total_chunks} processed successfully (retry)")
                                except Exception as retry_error:
                                    logger.error(f"Retry failed for chunk {chunk_index + 1}: {retry_error}")
                                    continue
                                
                    except Exception as e:
                        logger.error(f"Error processing chunk {chunk_index + 1}: {e}")
                        continue
                        
                finally:
                    # Clean up temporary WAV file
                    if temp_wav_path and os.path.exists(temp_wav_path):
                        try:
                            os.unlink(temp_wav_path)
                        except Exception as e:
                            logger.warning(f"Could not delete temporary file {temp_wav_path}: {e}")
            
            # Clear the audio from memory
            del audio
            
            if not all_transcripts:
                logger.error("No audio chunks could be transcribed successfully")
                logger.error(f"Total chunks attempted: {total_chunks}, Failed: {total_chunks}")
                logger.error("This video may contain primarily music, sound effects, or very unclear speech")
                return None
            
            # Combine all transcripts
            full_transcript = "\n".join(all_transcripts)
            logger.info(f"Speech-to-text conversion completed successfully ({len(all_transcripts)}/{total_chunks} chunks processed, {failed_chunks} failed)")
            
            if failed_chunks > 0:
                logger.warning(f"Note: {failed_chunks} chunk(s) contained no recognizable speech (music/silence/unclear audio)")
            
            return full_transcript
            
        except Exception as e:
            logger.error(f"Error converting audio to text: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            return None
    
    def cleanup_text_with_gemini(self, raw_text: str) -> Optional[str]:
        """
        Clean up and structure raw speech-to-text output using Gemini API
        
        Args:
            raw_text: Raw speech-to-text output
            
        Returns:
            Cleaned and structured text if successful, None otherwise
        """
        if not self.gemini_api_key:
            logger.warning("No Gemini API key provided, skipping text cleanup")
            return raw_text
        
        try:
            logger.info("Cleaning up text with Gemini API...")
            
            client = genai.Client(api_key=self.gemini_api_key)
            
            prompt = f"""
            Please clean up and structure the following raw speech-to-text transcript. 
            Make it more readable by:
            1. Adding proper punctuation and capitalization
            2. Breaking it into logical paragraphs
            3. Correcting obvious transcription errors
            4. Maintaining the original meaning and content
            5. Adding timestamps where natural breaks occur (use format [MM:SS])
            
            Raw transcript:
            {raw_text}
            
            Please provide a clean, well-structured transcript:
            """
            
            model = "gemini-2.0-flash-exp"
            contents = [
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)],
                ),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                response_modalities=["TEXT"],
            )
            
            response_parts = []
            for chunk in client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.candidates and chunk.candidates[0].content.parts:
                    response_parts.append(chunk.candidates[0].content.parts[0].text)
            
            cleaned_text = "".join(response_parts).strip()
            logger.info("Text cleanup completed")
            return cleaned_text
            
        except Exception as e:
            logger.error(f"Error cleaning text with Gemini API: {e}")
            logger.info("Returning original raw text")
            return raw_text
    
    def extract_transcript(self, video_url: str) -> Tuple[Optional[str], str, dict]:
        """
        Main method to extract transcript from YouTube video
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Tuple of (transcript_text, method_used, metadata)
        """
        # Extract video ID from URL
        video_id = self.extract_video_id(video_url)
        if not video_id:
            logger.error("Invalid YouTube URL provided")
            return None, "error", {}
        
        logger.info(f"Processing video: https://www.youtube.com/watch?v={video_id}")
        
        # Fetch video metadata
        metadata = self.get_video_metadata(video_id)
        
        # Step 1: Try to get transcript directly from YouTube
        transcript = self.get_video_transcript(video_id)
        if transcript:
            logger.info("Successfully extracted transcript from YouTube")
            return transcript, "youtube_transcript", metadata
        
        # Step 2: Fallback to audio download and speech-to-text
        logger.info("No transcript available, falling back to speech-to-text...")
        
        # Check FFmpeg availability before attempting audio processing
        if not self.ffmpeg_available:
            logger.error("Cannot use speech-to-text fallback: FFmpeg is not installed")
            logger.error(f"FFmpeg issue: {self.ffmpeg_error}")
            
            # Provide helpful installation instructions
            print("\n" + "!"*60)
            print("⚠️  SPEECH-TO-TEXT UNAVAILABLE")
            print("!"*60)
            print("FFmpeg is required for audio processing but is not installed.")
            print()
            print("Quick Fix Options:")
            print("1. Run the FFmpeg installer: install_ffmpeg.bat")
            print("2. Install via Chocolatey: choco install ffmpeg")
            print("3. Install via Scoop: scoop install ffmpeg")
            print("4. Manual installation from: https://ffmpeg.org/download.html")
            print()
            print("After installation, restart your terminal and try again.")
            print("!"*60)
            
            return None, "ffmpeg_missing", metadata
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Download audio
            audio_path = os.path.join(temp_dir, f"{video_id}.%(ext)s")
            if not self.download_audio(video_id, audio_path):
                logger.error("Failed to download audio")
                return None, "error", metadata
            
            # Find the downloaded audio file
            downloaded_files = [f for f in os.listdir(temp_dir) if f.startswith(video_id)]
            if not downloaded_files:
                logger.error("Audio file not found after download")
                return None, "error", metadata
            
            audio_file_path = os.path.join(temp_dir, downloaded_files[0])
            logger.info(f"Audio file downloaded: {audio_file_path}")
            
            # Give the system a moment to release any file handles
            import time
            time.sleep(1)
            
            # Convert audio to text
            raw_text = self.audio_to_text(audio_file_path)
            if not raw_text:
                logger.error("Failed to convert audio to text")
                return None, "error", metadata
            
            logger.info("Successfully converted audio to text")
            
            # Step 3: Clean up text with Gemini API if available
            if self.gemini_api_key:
                cleaned_text = self.cleanup_text_with_gemini(raw_text)
                if cleaned_text:
                    return cleaned_text, "speech_to_text_with_ai_cleanup", metadata
            
            return raw_text, "speech_to_text", metadata
    
    def _format_timestamp(self, seconds: float) -> str:
        """
        Convert seconds to MM:SS or HH:MM:SS format
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

def main():
    """
    Main function for command-line usage
    """
    if len(sys.argv) < 2:
        print("YouTube Transcript Extractor")
        print("Usage: python youtube_transcript_extractor.py <youtube_url> [gemini_api_key]")
        print("\nExamples:")
        print("  python youtube_transcript_extractor.py https://www.youtube.com/watch?v=VIDEO_ID")
        print("  python youtube_transcript_extractor.py https://youtu.be/VIDEO_ID YOUR_GEMINI_API_KEY")
        sys.exit(1)
    
    video_url = sys.argv[1]
    gemini_api_key = sys.argv[2] if len(sys.argv) > 2 else None
    
    if gemini_api_key:
        logger.info("Gemini API key provided - AI cleanup will be available")
    else:
        logger.info("No Gemini API key provided - AI cleanup will be skipped")
    
    extractor = YouTubeTranscriptExtractor(gemini_api_key=gemini_api_key)
    
    try:
        transcript, method, metadata = extractor.extract_transcript(video_url)
        
        if transcript:
            print(f"\n{'='*80}")
            print(f"TRANSCRIPT EXTRACTED USING: {method.upper()}")
            print(f"{'='*80}")
            print(f"Title: {metadata.get('title', 'N/A')}")
            print(f"Channel: {metadata.get('channel', 'N/A')}")
            print(f"Duration: {metadata.get('duration_string', 'N/A')}")
            print(f"Upload Date: {metadata.get('upload_date', 'N/A')}")
            print(f"Views: {metadata.get('view_count', 'N/A'):,}" if isinstance(metadata.get('view_count'), int) else f"Views: {metadata.get('view_count', 'N/A')}")
            print(f"Likes: {metadata.get('like_count', 'N/A'):,}" if isinstance(metadata.get('like_count'), int) else f"Likes: {metadata.get('like_count', 'N/A')}")
            print(f"VIDEO URL: {video_url}")
            print(f"{'='*80}")
            print(transcript)
            
            # Save to file with metadata
            output_file = "extracted_transcript.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"TRANSCRIPT EXTRACTION REPORT\n")
                f.write(f"{'='*80}\n\n")
                f.write(f"VIDEO INFORMATION\n")
                f.write(f"{'-'*80}\n")
                f.write(f"Title: {metadata.get('title', 'N/A')}\n")
                f.write(f"Channel: {metadata.get('channel', 'N/A')}\n")
                f.write(f"Channel ID: {metadata.get('channel_id', 'N/A')}\n")
                f.write(f"Duration: {metadata.get('duration_string', 'N/A')} ({metadata.get('duration', 0)} seconds)\n")
                f.write(f"Upload Date: {metadata.get('upload_date', 'N/A')}\n")
                f.write(f"View Count: {metadata.get('view_count', 'N/A'):,}\n" if isinstance(metadata.get('view_count'), int) else f"View Count: {metadata.get('view_count', 'N/A')}\n")
                f.write(f"Like Count: {metadata.get('like_count', 'N/A'):,}\n" if isinstance(metadata.get('like_count'), int) else f"Like Count: {metadata.get('like_count', 'N/A')}\n")
                f.write(f"Video URL: {video_url}\n")
                f.write(f"Thumbnail: {metadata.get('thumbnail', 'N/A')}\n")
                
                # Add description
                description = metadata.get('description', 'N/A')
                if description and description != 'N/A':
                    f.write(f"\nDESCRIPTION\n")
                    f.write(f"{'-'*80}\n")
                    f.write(f"{description}\n")
                
                # Add tags if available
                tags = metadata.get('tags', [])
                if tags:
                    f.write(f"\nTAGS\n")
                    f.write(f"{'-'*80}\n")
                    f.write(f"{', '.join(tags)}\n")
                
                # Add categories if available
                categories = metadata.get('categories', [])
                if categories:
                    f.write(f"\nCATEGORIES\n")
                    f.write(f"{'-'*80}\n")
                    f.write(f"{', '.join(categories)}\n")
                
                f.write(f"\n{'='*80}\n")
                f.write(f"EXTRACTION METHOD: {method.upper()}\n")
                f.write(f"{'='*80}\n\n")
                f.write(f"TRANSCRIPT\n")
                f.write(f"{'-'*80}\n")
                f.write(transcript)
            
            print(f"\nTranscript saved to: {output_file}")
        elif method == "ffmpeg_missing":
            print("\n" + "!"*60)
            print("❌ EXTRACTION FAILED: FFmpeg Not Installed")
            print("!"*60)
            print("This video has no transcript available, so speech-to-text")
            print("conversion is required. However, FFmpeg is not installed.")
            print()
            print("🔧 To fix this issue:")
            print("   1. Run: install_ffmpeg.bat")
            print("   2. Or install manually from: https://ffmpeg.org/download.html")
            print("   3. Restart your terminal after installation")
            print("   4. Try again with the same video URL")
            print()
            print("💡 Alternatively, try a different video that has transcripts available.")
            print("!"*60)
            sys.exit(1)
        else:
            print("Failed to extract transcript from the video")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()