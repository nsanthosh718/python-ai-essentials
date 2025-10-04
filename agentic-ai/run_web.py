#!/usr/bin/env python3
"""
Quick launcher for the Agentic AI Web Monitor
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    return True

def main():
    print("🚀 Starting Agentic AI Web Monitor...")
    
    # Check if requirements are installed
    try:
        import flask
        import flask_socketio
    except ImportError:
        print("📦 Installing dependencies...")
        if not install_requirements():
            return
    
    # Start the web server
    print("🌐 Starting web server at http://localhost:5000")
    print("📊 Open your browser to view the real-time dashboard")
    
    from web_monitor import app, socketio
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()