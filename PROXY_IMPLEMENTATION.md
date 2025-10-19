# Proxy Implementation - Complete Guide

## Problem Solved
YouTube blocks Digital Ocean and other cloud IPs. We've implemented rotating proxy support to bypass this.

## What's Been Done

### 1. Code Changes
- ✅ Added proxy rotation to `youtube_transcript_extractor.py`
- ✅ Added proxy support for both yt-dlp AND youtube-transcript-api
- ✅ Updated proxy list with 10 fresh proxies
- ✅ Added timeout and retry logic
- ✅ Removed cookie dependencies

### 2. Configuration
File: `enhanced_config.py`
```python
USE_PROXY = True
PROXY_LIST = [
    "http://47.88.3.19:8080",
    "http://47.251.43.115:33333",
    # ... 8 more proxies
]
PROXY_TIMEOUT = 15
```

### 3. New Tool: Proxy Updater
File: `update_proxies.py` - Auto-fetches fresh proxies from public sources

---

## Deployment to Digital Ocean

### Step 1: Commit and Push
```bash
git add .
git commit -m "Implement proxy rotation with timeout and better error handling"
git push origin main
```

### Step 2: Update Server
```bash
ssh root@137.184.46.113
cd ~/youtube_url_to_pdf
git pull origin main
pm2 restart fastapi-app
```

### Step 3: Monitor Logs
```bash
pm2 logs fastapi-app --lines 50
```

**Look for:**
- `INFO - Using proxy: http://47.88.3.19:8080`
- `INFO - Metadata fetched: <video title>`
- `INFO - Transcript extracted successfully`

---

## If Proxies Still Fail

Free proxies die quickly. Here are your options:

### Option A: Update Proxies (Free but manual)

Run the proxy updater on your server:
```bash
cd ~/youtube_url_to_pdf
python3 update_proxies.py
```

This will fetch and test new proxies. Copy the working ones to `enhanced_config.py`.

### Option B: Use Paid Proxies (Recommended for production)

**Best options:**
1. **Webshare.io** - $2.99/month for 10 residential proxies
   - Sign up: https://www.webshare.io/
   - Get proxies: Dashboard → Proxy List
   - Format: `http://username:password@proxy-server.com:port`

2. **Bright Data (formerly Luminati)** - Free tier available
   - Sign up: https://brightdata.com/
   - 500 free requests/month
   - Very reliable

3. **SmartProxy** - $8.50/month starter
   - Sign up: https://smartproxy.com/
   - 2GB traffic included

**To use paid proxies:**
1. Get proxy credentials from provider
2. Update `PROXY_LIST` in `enhanced_config.py`:
   ```python
   PROXY_LIST = [
       "http://username:password@gate.smartproxy.com:7000",
       "http://username:password@gate.smartproxy.com:7001",
   ]
   ```
3. Restart service: `pm2 restart fastapi-app`

### Option C: Disable Proxies Temporarily
If you need to test without proxies:
```python
# In enhanced_config.py
USE_PROXY = False
```

---

## Expected Behavior

### With Working Proxies ✅
- Request takes 3-8 seconds (proxy adds latency)
- Logs show: "Using proxy: http://..."
- Successfully extracts transcript
- Returns PDF with content

### With Dead Proxies ❌
- Timeout errors after 15 seconds
- "No route to host" or "Connection refused"
- Rotates to next proxy automatically
- May fail after trying all proxies

---

## Maintenance Schedule

**Daily:** Check service is working
**Weekly:** Update proxy list if seeing failures
**Monthly:** Consider paid proxy service if free proxies unreliable

---

## Current Status

✅ Code updated with proxy support
✅ Proxy rotation implemented
✅ Timeout/retry logic added
✅ Cookie dependencies removed
⏳ Waiting for you to push to GitHub
⏳ Then pull on Digital Ocean server
⏳ Then test with real video

---

## Quick Test Command

After deployment, test with:
```bash
curl -X POST "http://137.184.46.113:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url":"https://www.youtube.com/watch?v=jNQXAC9IVRw","prompt":"summary with 1 image"}' \
  --output result.zip && unzip -l result.zip
```

If it times out (> 30 seconds), proxies are dead → run `update_proxies.py` or switch to paid proxies.

---

## Recommended Next Step

For production reliability, I strongly recommend paid proxies ($3-9/month). Free proxies will always be unreliable. With paid proxies, you'll get:
- 99% uptime
- Fast speeds (< 2 sec overhead)
- No manual maintenance
- Residential IPs (never blocked)

Otherwise, you'll need to update the free proxy list every few days.
