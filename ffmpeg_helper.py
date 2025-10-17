#!/usr/bin/env python3
"""
FFmpeg Detection and Installation Helper
"""

import os
import subprocess
import sys
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

def check_ffmpeg_installation() -> Tuple[bool, Optional[str]]:
    """
    Check if FFmpeg is properly installed and accessible
    
    Returns:
        Tuple of (is_installed, error_message)
    """
    # Check for local FFmpeg installation first
    local_ffmpeg_paths = [
        os.path.join(os.getcwd(), "ffmpeg-8.0-essentials_build", "bin", "ffmpeg.exe"),
        os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe"),
        os.path.join(os.getcwd(), "ffmpeg", "ffmpeg.exe"),
        os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg"),
        os.path.join(os.getcwd(), "ffmpeg", "ffmpeg"),
    ]
    
    for ffmpeg_path in local_ffmpeg_paths:
        if os.path.exists(ffmpeg_path):
            try:
                result = subprocess.run([ffmpeg_path, '-version'], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=10)
                if result.returncode == 0:
                    # Also check for ffprobe in the same directory
                    ffprobe_path = ffmpeg_path.replace("ffmpeg", "ffprobe")
                    if os.path.exists(ffprobe_path):
                        probe_result = subprocess.run([ffprobe_path, '-version'], 
                                                    capture_output=True, 
                                                    text=True, 
                                                    timeout=10)
                        if probe_result.returncode == 0:
                            # Set environment variable for pydub to find local FFmpeg
                            os.environ['PATH'] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get('PATH', '')
                            return True, None
            except Exception:
                continue
    
    # Fall back to system PATH check
    try:
        # Check ffmpeg
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode != 0:
            return False, "FFmpeg found but not working properly"
            
        # Check ffprobe
        result = subprocess.run(['ffprobe', '-version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode != 0:
            return False, "FFprobe found but not working properly"
            
        return True, None
        
    except subprocess.TimeoutExpired:
        return False, "FFmpeg/FFprobe timed out (may be corrupted installation)"
    except FileNotFoundError:
        return False, "FFmpeg/FFprobe not found in system PATH or local directory"
    except Exception as e:
        return False, f"Error checking FFmpeg: {str(e)}"

def get_ffmpeg_install_instructions() -> str:
    """
    Get platform-specific FFmpeg installation instructions
    """
    if sys.platform.startswith('win'):
        return """
🔧 FFmpeg Installation Instructions for Windows:

Option 1: Using Chocolatey (Recommended)
   1. Install Chocolatey: https://chocolatey.org/install
   2. Run as Administrator: choco install ffmpeg
   3. Restart your terminal/PowerShell

Option 2: Using Scoop
   1. Install Scoop: https://scoop.sh/
   2. Run: scoop install ffmpeg

Option 3: Manual Installation
   1. Download from: https://www.gyan.dev/ffmpeg/builds/
   2. Extract to C:\\ffmpeg\\
   3. Add C:\\ffmpeg\\bin to your Windows PATH:
      - Press Win+R, type "sysdm.cpl"
      - Click "Environment Variables"
      - Under "System Variables", find "Path"
      - Click "Edit" → "New" → Add "C:\\ffmpeg\\bin"
      - Click "OK" and restart your terminal

Option 4: Using winget (Windows 10/11)
   winget install ffmpeg

After installation, restart your terminal and test with: ffmpeg -version
"""
    elif sys.platform.startswith('darwin'):
        return """
🔧 FFmpeg Installation Instructions for macOS:

Option 1: Using Homebrew (Recommended)
   brew install ffmpeg

Option 2: Using MacPorts
   sudo port install ffmpeg

After installation, test with: ffmpeg -version
"""
    else:  # Linux
        return """
🔧 FFmpeg Installation Instructions for Linux:

Ubuntu/Debian:
   sudo apt update && sudo apt install ffmpeg

CentOS/RHEL/Fedora:
   sudo yum install ffmpeg  # or dnf install ffmpeg

Arch Linux:
   sudo pacman -S ffmpeg

After installation, test with: ffmpeg -version
"""

def suggest_alternatives() -> str:
    """
    Suggest alternatives when FFmpeg is not available
    """
    return """
🔄 Alternative Solutions:

1. Use online transcript services:
   - YouTube's auto-generated captions (when available)
   - Third-party transcript services

2. Convert audio manually:
   - Use online audio converters to WAV format
   - Place the WAV file in the project directory
   - Modify the code to use the pre-converted file

3. Use cloud-based speech recognition:
   - Google Cloud Speech-to-Text
   - Azure Speech Services
   - AWS Transcribe

4. Install a Python-only audio library:
   - Consider using 'moviepy' instead of 'pydub'
   - Use 'librosa' for audio processing
"""

if __name__ == "__main__":
    print("🔍 Checking FFmpeg Installation...")
    is_installed, error_msg = check_ffmpeg_installation()
    
    if is_installed:
        print("✅ FFmpeg is properly installed and working!")
    else:
        print(f"❌ FFmpeg Issue: {error_msg}")
        print(get_ffmpeg_install_instructions())
        print(suggest_alternatives())