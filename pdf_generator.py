# PDF Generator with Text and Images
# Integrates Gemini text generation, image generation, and ReportLab

import os
import logging
import mimetypes
from typing import List, Dict, Tuple
from google import genai
from google.genai import types
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import re

logger = logging.getLogger(__name__)

class PDFGenerator:
    def __init__(self, text_api_key: str, image_api_key: str, temp_dir: str):
        """
        Initialize PDF Generator with separate API keys
        
        Args:
            text_api_key: Gemini API key for text generation
            image_api_key: Gemini API key for image generation
            temp_dir: Temporary directory for storing images
        """
        self.text_client = genai.Client(api_key=text_api_key)
        self.image_client = genai.Client(api_key=image_api_key)
        self.temp_dir = temp_dir
        self.generated_images = []
        
    def generate_structured_content(self, transcript: str, prompt: str) -> Dict:
        """
        Generate structured content based on transcript and prompt
        
        Returns:
            Dict with 'sections', 'image_prompts', and 'title'
        """
        logger.info("Generating structured content with Gemini...")
        
        system_prompt = f"""
You are a content writer who explains things in simple, easy-to-understand English. Based on the transcript and user instructions, create a clear document that anyone can read.

USER INSTRUCTIONS:
{prompt}

TRANSCRIPT:
{transcript[:5000]}

Please generate a JSON response with the following structure:
{{
    "title": "Simple Clear Title",
    "sections": [
        {{
            "heading": "Section Heading",
            "content": "Section content in simple paragraphs",
            "image_prompt": "Visual image description (or null if no image needed)"
        }}
    ]
}}

CRITICAL REQUIREMENTS:
1. Follow the user's instructions carefully
2. Use SIMPLE, CLEAR English - avoid complex words and jargon
3. Write like you're explaining to a friend - easy to understand
4. Create 4-5 logical sections with clear headings
5. Include image_prompt for EXACTLY 1 section only (no more, no less)
6. Choose the most important section for the image
7. For sections without images, set "image_prompt": null
8. Keep sentences short and simple
9. Use everyday words instead of difficult vocabulary

LANGUAGE STYLE:
- Use simple words: "use" not "utilize", "help" not "facilitate", "show" not "demonstrate"
- Keep sentences short (10-15 words average)
- Avoid technical jargon unless absolutely necessary
- Write in active voice: "We do this" not "This is done by us"
- Use conversational tone
- Break complex ideas into simple steps

STRICT IMAGE REQUIREMENTS - EXACTLY 1 IMAGE, ABSOLUTELY NO TEXT:
- Include image_prompt for EXACTLY 1 section (not more, not less)
- Image prompts MUST NOT request any text, words, labels, captions, or typography
- Focus on pure visual elements: objects, scenes, people, nature, concepts
- Use symbolic or metaphorical imagery to represent abstract concepts
- Examples: "A person climbing a mountain" instead of "Success diagram with text"
- Examples: "Interconnected gears and machinery" instead of "Workflow chart with labels"
- Examples: "A lightbulb glowing brightly" instead of "Innovation infographic"

Example image prompt format (NO TEXT):
"A professional photograph of [visual scene], featuring [physical objects/people/nature], with [lighting/mood/style]"
"""
        
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=system_prompt)],
            ),
        ]
        
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=-1),
            response_mime_type="application/json"
        )
        
        full_response = ""
        for chunk in self.text_client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        ):
            if chunk.text:
                full_response += chunk.text
        
        logger.info("Structured content generated")
        
        # Parse JSON response
        import json
        try:
            content_structure = json.loads(full_response)
            
            # Validate and enforce exactly 1 image
            sections = content_structure.get('sections', [])
            image_count = sum(1 for s in sections if s.get('image_prompt'))
            
            if image_count != 1:
                logger.warning(f"Content has {image_count} images, adjusting to exactly 1...")
                
                # Find sections with images
                sections_with_images = [i for i, s in enumerate(sections) if s.get('image_prompt')]
                sections_without_images = [i for i, s in enumerate(sections) if not s.get('image_prompt')]
                
                if image_count > 1:
                    # Remove extra images (keep only first one)
                    for idx in sections_with_images[1:]:
                        sections[idx]['image_prompt'] = None
                    logger.info("Reduced to exactly 1 image")
                
                elif image_count < 1 and len(sections_without_images) > 0:
                    # Add image to first section without one
                    idx = sections_without_images[0]
                    heading = sections[idx].get('heading', 'concept')
                    # Create a simple image prompt
                    sections[idx]['image_prompt'] = f"A professional photograph showing {heading.lower()}, clear and simple visual representation"
                    logger.info(f"Added 1 image prompt to reach exactly 1 image")
            
            return content_structure
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            # Fallback structure
            return {
                "title": "Generated Document",
                "sections": [
                    {
                        "heading": "Content",
                        "content": full_response,
                        "image_prompt": None
                    }
                ]
            }
    
    def generate_image(self, prompt: str, index: int) -> str:
        """
        Generate image using Gemini 2.5 Flash Image model
        
        Returns:
            Path to generated image file
        """
        import time
        
        # Add delay before generating to avoid rate limits
        # Wait longer for subsequent images
        if index > 0:
            wait_time = 10 * index  # 10 seconds between each image
            logger.info(f"Waiting {wait_time} seconds before generating image {index + 1} (rate limit prevention)...")
            time.sleep(wait_time)
        
        logger.info(f"Generating image {index + 1}: {prompt[:80]}...")
        
        max_retries = 1  # Reduce retries since we're adding delays
        for attempt in range(max_retries):
            try:
                import mimetypes
                
                # Add strict NO TEXT instruction to the prompt
                enhanced_prompt = f"""{prompt}

CRITICAL REQUIREMENTS:
- NO text, letters, words, or any written characters in the image
- NO labels, captions, or typography
- Pure visual representation only
- Clean, professional, high-quality image
- Focus on visual elements, objects, scenes, and concepts
- If the concept requires explanation, use symbolic or metaphorical imagery instead of text"""
                
                contents = [
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=enhanced_prompt),
                        ],
                    ),
                ]
                
                generate_content_config = types.GenerateContentConfig(
                    response_modalities=[
                        "IMAGE",
                    ],
                )
                
                # Generate image
                for chunk in self.image_client.models.generate_content_stream(
                    model="gemini-2.5-flash-image",
                    contents=contents,
                    config=generate_content_config,
                ):
                    if (
                        chunk.candidates is None
                        or chunk.candidates[0].content is None
                        or chunk.candidates[0].content.parts is None
                    ):
                        continue
                    
                    if (chunk.candidates[0].content.parts[0].inline_data and 
                        chunk.candidates[0].content.parts[0].inline_data.data):
                        
                        inline_data = chunk.candidates[0].content.parts[0].inline_data
                        data_buffer = inline_data.data
                        file_extension = mimetypes.guess_extension(inline_data.mime_type) or '.jpg'
                        
                        image_path = os.path.join(self.temp_dir, f"generated_image_{index}{file_extension}")
                        
                        with open(image_path, 'wb') as f:
                            f.write(data_buffer)
                        
                        self.generated_images.append(image_path)
                        logger.info(f"✓ Image {index + 1} generated successfully: {image_path}")
                        return image_path
                
                logger.warning(f"No image data received (attempt {attempt + 1}/{max_retries})")
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error generating image (attempt {attempt + 1}/{max_retries}): {error_msg[:200]}")
                
                # Check if it's a quota/rate limit error
                if '429' in error_msg or 'RESOURCE_EXHAUSTED' in error_msg or 'quota' in error_msg.lower():
                    logger.warning(f"Rate limit hit. Waiting 60 seconds before retry...")
                    time.sleep(60)  # Wait 1 minute for quota to reset
                elif attempt < max_retries - 1:
                    logger.info(f"Waiting 5 seconds before retry...")
                    time.sleep(5)
                    continue
        
        logger.error(f"Failed to generate image after {max_retries} attempts")
        return None
    
    def create_pdf_elements(self, content_structure: Dict, metadata: Dict) -> List:
        """
        Create ReportLab elements from structured content
        
        Returns:
            List of ReportLab flowable elements
        """
        logger.info("Creating PDF elements...")
        
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            alignment=TA_JUSTIFY,
            spaceAfter=12,
            leading=16
        )
        
        metadata_style = ParagraphStyle(
            'Metadata',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#666666'),
            spaceAfter=6
        )
        
        # Add title
        title = content_structure.get('title', 'Generated Document')
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Add metadata
        if metadata:
            meta_data = [
                f"<b>Video:</b> {metadata.get('title', 'N/A')}",
                f"<b>Channel:</b> {metadata.get('channel', 'N/A')}",
                f"<b>Duration:</b> {metadata.get('duration_string', 'N/A')}"
            ]
            for meta in meta_data:
                elements.append(Paragraph(meta, metadata_style))
            elements.append(Spacer(1, 0.3 * inch))
        
        # Add horizontal line
        from reportlab.platypus import HRFlowable
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cccccc')))
        elements.append(Spacer(1, 0.2 * inch))
        
        # Add sections with images
        sections = content_structure.get('sections', [])
        for idx, section in enumerate(sections):
            # Section heading
            heading = section.get('heading', f'Section {idx + 1}')
            elements.append(Paragraph(heading, heading_style))
            elements.append(Spacer(1, 0.1 * inch))
            
            # Section content
            content = section.get('content', '')
            # Split into paragraphs
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    elements.append(Paragraph(para.strip(), body_style))
                    elements.append(Spacer(1, 0.1 * inch))
            
            # Generate and add image if specified
            image_prompt = section.get('image_prompt')
            if image_prompt and image_prompt.strip():
                # Count current images to use as index
                current_image_index = len(self.generated_images)
                logger.info(f"Section '{heading}' needs image #{current_image_index + 1}: {image_prompt[:80]}...")
                
                image_path = self.generate_image(image_prompt, current_image_index)
                
                if image_path and os.path.exists(image_path):
                    # Add image with caption
                    try:
                        img = Image(image_path, width=5 * inch, height=2.8 * inch)
                        elements.append(Spacer(1, 0.2 * inch))
                        elements.append(img)
                        
                        # Add caption
                        caption_style = ParagraphStyle(
                            'Caption',
                            parent=styles['Normal'],
                            fontSize=9,
                            textColor=colors.HexColor('#666666'),
                            alignment=TA_CENTER,
                            spaceAfter=12,
                            italic=True
                        )
                        caption_text = f"<i>Image {current_image_index + 1}: {heading}</i>"
                        elements.append(Paragraph(caption_text, caption_style))
                        elements.append(Spacer(1, 0.2 * inch))
                        logger.info(f"✓ Image {current_image_index + 1} successfully added to PDF for section '{heading}'")
                    except Exception as e:
                        logger.error(f"Error adding image to PDF: {e}")
                else:
                    logger.warning(f"❌ Image generation failed for section '{heading}' - continuing without image")
            else:
                logger.info(f"Section '{heading}' has no image prompt (as expected)")
            
            # Add spacing between sections
            elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def generate_pdf(self, transcript: str, metadata: Dict, prompt: str, output_path: str):
        """
        Main method to generate PDF with text and images
        
        Args:
            transcript: Raw transcript text
            metadata: Video metadata
            prompt: User's instructions for PDF generation
            output_path: Path to save PDF
        """
        logger.info("Starting PDF generation...")
        logger.info(f"Transcript length: {len(transcript)} characters")
        logger.info(f"Using simple, easy-to-understand English")
        logger.info(f"Limiting to exactly 1 image")
        logger.info(f"Prompt: {prompt[:200]}...")
        
        try:
            # Step 1: Generate structured content
            content_structure = self.generate_structured_content(transcript, prompt)
            
            # Count sections with images
            sections_with_images = sum(1 for s in content_structure.get('sections', []) 
                                      if s.get('image_prompt'))
            total_sections = len(content_structure.get('sections', []))
            logger.info(f"Content structure: {total_sections} sections, {sections_with_images} with image prompts (target: 1)")
            
            # Step 2: Create PDF
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=50,
            )
            
            # Step 3: Create elements
            elements = self.create_pdf_elements(content_structure, metadata)
            
            # Step 4: Build PDF
            doc.build(elements)
            
            logger.info(f"✓ PDF generated successfully: {output_path}")
            logger.info(f"✓ Total images generated: {len(self.generated_images)} (expected: 1)")
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}", exc_info=True)
            raise
    
    def cleanup(self):
        """Clean up generated images"""
        for image_path in self.generated_images:
            try:
                if os.path.exists(image_path):
                    os.remove(image_path)
                    logger.info(f"Cleaned up image: {image_path}")
            except Exception as e:
                logger.error(f"Error cleaning up image {image_path}: {e}")
