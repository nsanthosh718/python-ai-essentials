#!/usr/bin/env python3
"""
Secure API Key Setup for OpenAI Integration
"""

import os
from pathlib import Path

def setup_openai_key():
    """Securely setup OpenAI API key"""
    print("🔐 OpenAI API Key Setup")
    print("=" * 40)
    
    # Check if .env file exists
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ .env file found")
        # Load existing key
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY" in content:
                print("✅ OpenAI API key is configured")
                return True
    
    print("⚠️  OpenAI API key not found")
    print("\n📋 To use OpenAI features:")
    print("1. Create a .env file in this directory")
    print("2. Add your API key: OPENAI_API_KEY=your-key-here")
    print("3. Never commit the .env file to version control")
    
    # Offer to create .env file
    create_env = input("\n❓ Create .env file now? (y/n): ").lower().strip()
    
    if create_env == 'y':
        api_key = input("🔑 Enter your OpenAI API key: ").strip()
        
        if api_key:
            with open(".env", "w") as f:
                f.write(f"OPENAI_API_KEY={api_key}\n")
            print("✅ .env file created successfully")
            print("🔒 Your API key is now secure and not tracked by git")
            return True
        else:
            print("❌ No API key provided")
    
    print("\n💡 You can still use the system in mock mode without an API key")
    return False

def load_env_vars():
    """Load environment variables from .env file"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

if __name__ == "__main__":
    setup_openai_key()