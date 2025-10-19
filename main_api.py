# FastAPI YouTube Transcript to PDF Service
# Install: pip install fastapi uvicorn python-multipart

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import tempfile
import shutil
from datetime import datetime
import logging

# Import existing modules
from youtube_transcript_extractor import YouTubeTranscriptExtractor
import enhanced_config as config
from pdf_generator import PDFGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="YouTube Transcript to PDF Service",
    description="Extract YouTube transcripts and generate structured PDFs with images",
    version="1.0.0"
)

class TranscriptRequest(BaseModel):
    youtube_url: str
    prompt: str

    class Config:
        json_schema_extra = {
            "example": {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "prompt": "Create a detailed summary with key points. Include relevant images for main concepts. Format as: Introduction, Main Points (with subheadings), and Conclusion."
            }
        }

def cleanup_temp_files(temp_dir: str):
    """Clean up temporary files and directories"""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        logger.error(f"Error cleaning up temp files: {e}")

@app.get("/")
async def root():
    return {
        "service": "YouTube Transcript to PDF",
        "status": "running",
        "endpoints": {
            "generate": "/generate (POST)",
            "health": "/health (GET)"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/generate")
async def generate_transcript_pdf(
    request: TranscriptRequest,
    background_tasks: BackgroundTasks
):
    """
    Generate transcript and PDF from YouTube URL
    
    - **youtube_url**: YouTube video URL
    - **prompt**: Instructions for PDF generation (formatting, style, content focus)
    
    Returns: ZIP file containing extracted_transcript.txt and structured.pdf
    """
    
    temp_dir = None
    
    try:
        # Create temporary directory for this request
        temp_dir = tempfile.mkdtemp(prefix="youtube_pdf_")
        logger.info(f"Created temp directory: {temp_dir}")
        
        # Define output paths
        transcript_path = os.path.join(temp_dir, "extracted_transcript.txt")
        pdf_path = os.path.join(temp_dir, "structured.pdf")
        zip_path = os.path.join(temp_dir, "result.zip")
        
        # Step 1: Extract YouTube transcript
        logger.info(f"Extracting transcript from: {request.youtube_url}")
        
        # Check if cookies file exists
        cookies_path = None
        if hasattr(config, 'COOKIES_FILE'):
            cookies_file = config.COOKIES_FILE
            # Try relative path first
            if os.path.exists(cookies_file):
                cookies_path = cookies_file
            # Try absolute path in /root/ for Linux deployment
            elif os.path.exists(f"/root/{cookies_file}"):
                cookies_path = f"/root/{cookies_file}"
            # Try in project directory
            elif os.path.exists(os.path.join(os.path.dirname(__file__), cookies_file)):
                cookies_path = os.path.join(os.path.dirname(__file__), cookies_file)
        
        extractor = YouTubeTranscriptExtractor(
            gemini_api_key=config.GEMINI_API_KEY,
            cookies_path=cookies_path
        )
        
        result = extractor.extract_transcript(request.youtube_url)
        transcript, method, metadata = result
        
        if not transcript:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to extract transcript. Method: {method}. Please check if the video is available and has captions."
            )
        
        logger.info(f"Transcript extracted successfully using method: {method}")
        
        # Step 2: Save raw transcript
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(f"TRANSCRIPT EXTRACTION REPORT\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"VIDEO INFORMATION\n")
            f.write(f"{'-'*80}\n")
            f.write(f"Title: {metadata.get('title', 'N/A')}\n")
            f.write(f"Channel: {metadata.get('channel', 'N/A')}\n")
            f.write(f"Duration: {metadata.get('duration_string', 'N/A')}\n")
            f.write(f"Views: {metadata.get('view_count', 'N/A'):,}\n" if isinstance(metadata.get('view_count'), int) else f"Views: {metadata.get('view_count', 'N/A')}\n")
            f.write(f"Video URL: {request.youtube_url}\n")
            f.write(f"\n{'='*80}\n")
            f.write(f"EXTRACTION METHOD: {method.upper()}\n")
            f.write(f"{'='*80}\n\n")
            f.write(f"TRANSCRIPT\n")
            f.write(f"{'-'*80}\n")
            f.write(transcript)
        
        logger.info("Transcript saved to file")
        
        # Step 3: Generate PDF with images
        logger.info("Generating PDF with text and images...")
        pdf_generator = PDFGenerator(
            text_api_key=config.GEMINI_TEXT_API_KEY,
            image_api_key=config.GEMINI_IMAGE_API_KEY,
            temp_dir=temp_dir
        )
        
        pdf_generator.generate_pdf(
            transcript=transcript,
            metadata=metadata,
            prompt=request.prompt,
            output_path=pdf_path
        )
        
        logger.info("PDF generated successfully")
        
        # Step 4: Create ZIP file with both outputs
        import zipfile
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(transcript_path, "extracted_transcript.txt")
            zipf.write(pdf_path, "structured.pdf")
        
        logger.info("ZIP file created")
        
        # Schedule cleanup after response is sent
        background_tasks.add_task(cleanup_temp_files, temp_dir)
        
        # Return ZIP file
        return FileResponse(
            path=zip_path,
            media_type="application/zip",
            filename=f"transcript_pdf_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
            background=background_tasks
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        if temp_dir:
            cleanup_temp_files(temp_dir)
        raise
        
    except Exception as e:
        logger.error(f"Error generating transcript/PDF: {str(e)}", exc_info=True)
        if temp_dir:
            cleanup_temp_files(temp_dir)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)
