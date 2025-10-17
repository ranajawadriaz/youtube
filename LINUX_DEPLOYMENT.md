# Linux Production Deployment Guide

## System Requirements
- Ubuntu 20.04+ / Debian 11+ / CentOS 8+ (or compatible)
- Python 3.10+
- 2GB RAM minimum (4GB recommended)
- 10GB disk space

## Installation Steps

### 1. Update System and Install System Dependencies

**For Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv ffmpeg portaudio19-dev build-essential
```

**For CentOS/RHEL:**
```bash
sudo yum update
sudo yum install -y python3-pip python3-virtualenv ffmpeg portaudio-devel gcc
```

**For Alpine Linux:**
```bash
sudo apk update
sudo apk add python3 py3-pip ffmpeg portaudio-dev build-base
```

### 2. Create Project Directory
```bash
mkdir -p /opt/youtube-transcript-api
cd /opt/youtube-transcript-api
```

### 3. Upload Project Files
Upload all project files to `/opt/youtube-transcript-api/`:
- main_api.py
- pdf_generator.py
- youtube_transcript_extractor.py
- enhanced_config.py
- requirements-linux.txt

### 4. Set Up Python Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements-linux.txt
```

### 6. Configure Environment Variables
Create `.env` file or set environment variables:
```bash
export GEMINI_API_KEY="AIzaSyDFqnd7vddPTNZjvSLCXZ2xHyOubHlaKlc"
export GEMINI_TEXT_API_KEY="AIzaSyBAksL_56Q40LbQXn2qgvxlEdiWCXXxoGo"
export GEMINI_IMAGE_API_KEY="AIzaSyB6_Wja8c0UZYoouayNYC5La4FIiL3NCy4"
```

### 7. Test FFmpeg Installation
```bash
ffmpeg -version
```
Should display version 4.0+ or higher.

### 8. Create Temp Directories
```bash
mkdir -p temp_downloads
mkdir -p temp_pdfs
chmod 755 temp_downloads temp_pdfs
```

## Running the Service

### Development Mode
```bash
source venv/bin/activate
uvicorn main_api:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode (Manual)
```bash
source venv/bin/activate
uvicorn main_api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Production Mode with Systemd (Recommended)

Create `/etc/systemd/system/youtube-transcript-api.service`:

```ini
[Unit]
Description=YouTube Transcript API Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/youtube-transcript-api
Environment="PATH=/opt/youtube-transcript-api/venv/bin"
Environment="GEMINI_API_KEY=AIzaSyDFqnd7vddPTNZjvSLCXZ2xHyOubHlaKlc"
Environment="GEMINI_TEXT_API_KEY=AIzaSyBAksL_56Q40LbQXn2qgvxlEdiWCXXxoGo"
Environment="GEMINI_IMAGE_API_KEY=AIzaSyB6_Wja8c0UZYoouayNYC5La4FIiL3NCy4"
ExecStart=/opt/youtube-transcript-api/venv/bin/uvicorn main_api:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable youtube-transcript-api
sudo systemctl start youtube-transcript-api
sudo systemctl status youtube-transcript-api
```

View logs:
```bash
sudo journalctl -u youtube-transcript-api -f
```

## Nginx Reverse Proxy (Optional but Recommended)

Install Nginx:
```bash
sudo apt-get install nginx  # Ubuntu/Debian
sudo yum install nginx      # CentOS/RHEL
```

Create `/etc/nginx/sites-available/youtube-transcript-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Change this

    client_max_body_size 100M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Increase timeouts for long-running requests
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/youtube-transcript-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Firewall Configuration

**UFW (Ubuntu):**
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (if using SSL)
sudo ufw enable
```

**Firewalld (CentOS):**
```bash
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## SSL/TLS with Let's Encrypt (Recommended for Production)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Testing the API

### Health Check
```bash
curl http://localhost:8000/
```

### Generate Transcript and PDF
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "prompt": "Create a simple summary with exactly 1 image"
  }' \
  --output result.zip
```

Extract and verify:
```bash
unzip result.zip
ls -lh transcript.txt structured.pdf
```

## Monitoring and Maintenance

### Check Service Status
```bash
sudo systemctl status youtube-transcript-api
```

### View Logs
```bash
sudo journalctl -u youtube-transcript-api -n 100 --no-pager
```

### Restart Service
```bash
sudo systemctl restart youtube-transcript-api
```

### Disk Space Monitoring
```bash
df -h /opt/youtube-transcript-api
du -sh temp_*
```

### Clean Up Temp Files (if needed)
```bash
find temp_downloads -type f -mtime +1 -delete
find temp_pdfs -type d -mtime +1 -exec rm -rf {} +
```

### Set Up Log Rotation
Create `/etc/logrotate.d/youtube-transcript-api`:

```
/var/log/youtube-transcript-api/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 0640 www-data www-data
}
```

## Performance Tuning

### Increase Worker Count (for high traffic)
Edit systemd service file:
```
ExecStart=/opt/youtube-transcript-api/venv/bin/uvicorn main_api:app --host 0.0.0.0 --port 8000 --workers 8
```

### Optimize FFmpeg
Set environment variable:
```
Environment="FFMPEG_THREADS=2"
```

## Troubleshooting

### FFmpeg Not Found
```bash
which ffmpeg
sudo ln -s /usr/bin/ffmpeg /usr/local/bin/ffmpeg
```

### Permission Issues
```bash
sudo chown -R www-data:www-data /opt/youtube-transcript-api
sudo chmod -R 755 /opt/youtube-transcript-api
```

### Port Already in Use
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Python Package Issues
```bash
source venv/bin/activate
pip install --upgrade --force-reinstall -r requirements-linux.txt
```

## Digital Ocean Specific Setup

### 1. Create Droplet
- Choose Ubuntu 22.04 LTS
- Select at least 2GB RAM droplet
- Add SSH key for access

### 2. Initial Server Setup
```bash
ssh root@your-droplet-ip
adduser youtube-api
usermod -aG sudo youtube-api
ufw allow OpenSSH
ufw enable
```

### 3. Deploy Application
```bash
su - youtube-api
git clone <your-repo>  # or upload files
cd <project-directory>
# Follow installation steps above
```

### 4. Configure Domain (Optional)
- Add A record in Digital Ocean DNS
- Point to droplet IP address
- Wait for DNS propagation (5-30 minutes)
- Configure Nginx and SSL as shown above

## Security Best Practices

1. **Never commit API keys to version control**
2. Use environment variables or secure vaults
3. Enable UFW/firewall
4. Keep system updated: `sudo apt-get update && sudo apt-get upgrade`
5. Use SSL/TLS in production
6. Restrict SSH to key-based authentication
7. Set up fail2ban for brute force protection:
   ```bash
   sudo apt-get install fail2ban
   sudo systemctl enable fail2ban
   ```

## API Endpoints

### POST /generate
Generate transcript and PDF from YouTube URL.

**Request:**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "prompt": "Your prompt for content generation with exactly 1 image"
}
```

**Response:**
- Content-Type: application/zip
- Contains: transcript.txt and structured.pdf

### GET /
Health check endpoint.

**Response:**
```json
{
  "message": "YouTube Transcript Extractor API is running"
}
```

## Support

For issues or questions, check:
1. Service logs: `sudo journalctl -u youtube-transcript-api -f`
2. Nginx logs: `sudo tail -f /var/log/nginx/error.log`
3. System logs: `sudo dmesg | tail`
