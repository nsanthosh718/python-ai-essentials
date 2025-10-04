"""
Simple screenshot generator with basic text
"""

from PIL import Image, ImageDraw
import os

def create_simple_screenshot(title, description, filename, size=(1200, 800)):
    """Create a simple screenshot with title and description"""
    
    # Create image with dark background
    img = Image.new('RGB', size, color='#1F2937')
    draw = ImageDraw.Draw(img)
    
    # Draw title (large text)
    draw.text((100, 200), title, fill='#3B82F6', anchor="lt")
    
    # Draw description
    draw.text((100, 300), description, fill='#9CA3AF', anchor="lt")
    
    # Draw AcmeForce branding
    draw.text((100, 500), "AcmeForce Agents - Revolutionary AI", fill='#10B981', anchor="lt")
    
    # Add some visual elements
    draw.rectangle([50, 50, size[0]-50, size[1]-50], outline='#374151', width=5)
    draw.rectangle([80, 150, size[0]-80, 180], fill='#3B82F6')
    
    # Save image
    img.save(filename)
    print(f"Created {filename}")

def generate_all_simple():
    """Generate all simple screenshots"""
    
    screenshots = [
        ("AcmeForceAgents Homepage", "Revolutionary AI System Landing Page", "homepage.png"),
        ("Interactive Demo", "Try AI Agents in Real-Time", "demo.png"),
        ("Pricing Plans", "Choose Your AI Transformation", "pricing.png"),
        ("Agent Dashboard", "Command Your AI Fleet", "dashboard.png")
    ]
    
    for title, desc, filename in screenshots:
        create_simple_screenshot(title, desc, filename)

if __name__ == "__main__":
    generate_all_simple()