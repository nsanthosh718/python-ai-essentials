"""
Generate placeholder screenshots for README
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_screenshot(title, description, filename, size=(1200, 800)):
    """Create a placeholder screenshot with title and description"""
    
    # Create image with dark background
    img = Image.new('RGB', size, color='#111827')
    draw = ImageDraw.Draw(img)
    
    # Use default font with larger size
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        desc_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        brand_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
        brand_font = ImageFont.load_default()
    
    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (size[0] - title_width) // 2
    draw.text((title_x, 200), title, fill='#3B82F6', font=title_font)
    
    # Draw description
    desc_bbox = draw.textbbox((0, 0), description, font=desc_font)
    desc_width = desc_bbox[2] - desc_bbox[0]
    desc_x = (size[0] - desc_width) // 2
    draw.text((desc_x, 300), description, fill='#9CA3AF', font=desc_font)
    
    # Draw AcmeForce branding
    brand_text = "AcmeForce Agents"
    brand_bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_width = brand_bbox[2] - brand_bbox[0]
    brand_x = (size[0] - brand_width) // 2
    draw.text((brand_x, 500), brand_text, fill='#10B981', font=brand_font)
    
    # Add border
    draw.rectangle([10, 10, size[0]-10, size[1]-10], outline='#374151', width=3)
    
    # Save image
    img.save(filename)
    print(f"Created {filename}")

def generate_all_placeholders():
    """Generate all placeholder screenshots"""
    
    screenshots = [
        {
            "title": "AcmeForceAgents Homepage",
            "description": "Revolutionary AI System Landing Page",
            "filename": "homepage.png"
        },
        {
            "title": "Interactive Demo",
            "description": "Try AI Agents in Real-Time",
            "filename": "demo.png"
        },
        {
            "title": "Pricing Plans",
            "description": "Choose Your AI Transformation",
            "filename": "pricing.png"
        },
        {
            "title": "Agent Dashboard",
            "description": "Command Your AI Fleet",
            "filename": "dashboard.png"
        }
    ]
    
    for screenshot in screenshots:
        create_placeholder_screenshot(
            screenshot["title"],
            screenshot["description"], 
            screenshot["filename"]
        )

if __name__ == "__main__":
    generate_all_placeholders()