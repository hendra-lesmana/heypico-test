#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import sys

def create_env_file():
    """Create a .env file from .env.example if it doesn't exist"""
    if os.path.exists(".env"):
        print("[✓] .env file already exists")
        return
    
    if not os.path.exists(".env.example"):
        print("[✗] .env.example file not found")
        return
    
    shutil.copy(".env.example", ".env")
    print("[✓] Created .env file from .env.example")
    print("    Please edit the .env file and add your Google Maps API key")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import dotenv
        import requests
        import pydantic
        import googlemaps
        print("[✓] All required Python packages are installed")
    except ImportError as e:
        print("[✗] Missing dependency: {}".format(str(e)))
        print("    Please run: pip install -r requirements.txt")

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/version")
        if response.status_code == 200:
            print("[✓] Ollama is running")
        else:
            print("[✗] Ollama is installed but not running")
            print("    Please start Ollama with: ollama serve")
    except:
        print("[✗] Ollama is not running or not installed")
        print("    Please install Ollama: https://ollama.ai/download")
        print("    Or check setup_ollama.md for instructions")

def main():
    """Initialize the application"""
    print("Initializing LLM with Google Maps Integration...\n")
    
    # Create .env file
    create_env_file()
    
    # Check dependencies
    check_dependencies()
    
    # Check Ollama
    check_ollama()
    
    print("\nSetup complete! To start the application, run:")
    print("python -m app.main")
    print("\nThe application will be available at http://localhost:8000")

if __name__ == "__main__":
    main()