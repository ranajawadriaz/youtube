# Test script for FastAPI service

import requests
import json

# API endpoint
API_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_generate():
    """Test PDF generation"""
    print("Testing PDF generation...")
    
    # Request payload
    payload = {
        "youtube_url": "https://www.youtube.com/watch?v=jNQXAC9IVRw",
        "prompt": """
Create a simple, easy-to-read document with clear sections.

Write in simple English that anyone can understand. Keep it short and clear.

Include exactly 1 image for the most important part.

Use a friendly, conversational tone.
"""
    }
    
    print(f"Request payload:")
    print(json.dumps(payload, indent=2))
    print("\nSending request... (this may take 1-2 minutes)")
    
    response = requests.post(
        f"{API_URL}/generate",
        json=payload,
        timeout=300  # 5 minutes timeout
    )
    
    if response.status_code == 200:
        # Save the ZIP file
        filename = "result.zip"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"\n✅ Success! Files saved to: {filename}")
        print("Extract the ZIP to get:")
        print("  - extracted_transcript.txt")
        print("  - structured.pdf")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    print("=" * 60)
    print("FastAPI YouTube Transcript to PDF - Test Script")
    print("=" * 60)
    print()
    
    test_health()
    test_generate()
