#!/bin/bash
# Quick Cookie Setup Script for YouTube API on Digital Ocean

echo "==================================================="
echo "YouTube Cookie Setup for Bot Detection Fix"
echo "==================================================="
echo ""

# Check if cookies.txt exists
if [ -f "cookies.txt" ]; then
    echo "✅ Found cookies.txt in current directory"
    
    # Set permissions
    chmod 600 cookies.txt
    echo "✅ Set permissions to 600"
    
    # Show first few lines (non-sensitive)
    echo ""
    echo "Cookie file preview:"
    head -3 cookies.txt
    echo ""
    
    # Validate format
    if head -1 cookies.txt | grep -q "Netscape"; then
        echo "✅ Cookie file format is correct (Netscape format)"
    else
        echo "⚠️  WARNING: Cookie file may not be in correct format"
        echo "   First line should be: # Netscape HTTP Cookie File"
    fi
    
    # Check if cookies are for YouTube
    if grep -q "youtube.com" cookies.txt; then
        echo "✅ Cookies contain YouTube domains"
    else
        echo "❌ ERROR: Cookies don't contain YouTube domains"
        echo "   Make sure you exported cookies from youtube.com"
    fi
    
    echo ""
    echo "Next steps:"
    echo "1. Restart your service: pm2 restart fastapi-app"
    echo "2. Check logs: pm2 logs fastapi-app --lines 20"
    echo "3. Look for: 'Using cookies from: /root/cookies.txt'"
    echo ""
    
elif [ -f "/root/cookies.txt" ]; then
    echo "✅ Found cookies.txt in /root/"
    echo "File is already in the correct location"
    
else
    echo "❌ cookies.txt not found!"
    echo ""
    echo "Please follow these steps:"
    echo ""
    echo "STEP 1: Export cookies from your browser"
    echo "  - Install browser extension: 'Get cookies.txt LOCALLY'"
    echo "  - Go to youtube.com (make sure you're logged in)"
    echo "  - Click extension icon and export cookies"
    echo "  - Save as cookies.txt"
    echo ""
    echo "STEP 2: Upload to server"
    echo "  From your local machine, run:"
    echo "  scp cookies.txt root@YOUR_SERVER_IP:/root/"
    echo ""
    echo "STEP 3: Run this script again"
    echo "  bash setup_cookies.sh"
    echo ""
fi

# Check if yt-dlp is installed
if command -v yt-dlp &> /dev/null; then
    echo "✅ yt-dlp is installed"
else
    echo "⚠️  yt-dlp not found - installing..."
    pip install -U yt-dlp
fi

echo ""
echo "==================================================="
echo "For detailed instructions, see:"
echo "YOUTUBE_COOKIE_SETUP.md"
echo "==================================================="
