#!/usr/bin/env python3

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_maps_api():
    """Test the Google Maps API connection"""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("[✗] Google Maps API key not configured")
        print("    Please add your API key to the .env file")
        return False
    
    # Test the Places API with a simple query
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=pizza&key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get("status") == "OK":
            print("[✓] Google Maps API connection successful")
            return True
        elif data.get("status") == "REQUEST_DENIED":
            print(f"[✗] Google Maps API request denied: {data.get('error_message')}")
            return False
        else:
            print(f"[✗] Google Maps API error: {data.get('status')}")
            return False
    except Exception as e:
        print(f"[✗] Error connecting to Google Maps API: {str(e)}")
        return False

def test_ollama_api():
    """Test the Ollama API connection"""
    host = os.getenv("OLLAMA_HOST", "http://localhost")
    port = os.getenv("OLLAMA_PORT", "11434")
    model = os.getenv("OLLAMA_MODEL", "llama3")
    
    # Check if Ollama is running
    try:
        response = requests.get(f"{host}:{port}/api/version")
        if response.status_code != 200:
            print("[✗] Ollama is not running")
            return False
    except:
        print("[✗] Ollama is not running")
        return False
    
    # Check if the model is available
    try:
        response = requests.post(
            f"{host}:{port}/api/generate",
            json={
                "model": model,
                "prompt": "Hello, world!",
                "stream": False
            }
        )
        
        if response.status_code == 200:
            print(f"[✓] Ollama API connection successful with model {model}")
            return True
        else:
            print(f"[✗] Ollama API error: {response.text}")
            return False
    except Exception as e:
        print(f"[✗] Error connecting to Ollama API: {str(e)}")
        return False

def test_fastapi_server():
    """Test if the FastAPI server is running"""
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code == 200:
            print("[✓] FastAPI server is running")
            return True
        else:
            print(f"[✗] FastAPI server returned status code {response.status_code}")
            return False
    except:
        print("[✗] FastAPI server is not running")
        print("    Start the server with: python -m app.main")
        return False

def test_llm_endpoint():
    """Test the LLM endpoint with a sample query"""
    if not test_fastapi_server():
        return False
    
    try:
        response = requests.post(
            "http://localhost:8000/api/llm",
            json={"prompt": "Where can I find pizza near Central Park?"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("[✓] LLM endpoint is working")
            print(f"    Response: {data.get('text')[:100]}...")
            
            if data.get('locations') and data.get('locations').get('places'):
                print(f"    Found {len(data.get('locations').get('places'))} places")
            
            if data.get('map_html'):
                print("    Map HTML generated successfully")
            
            return True
        else:
            print(f"[✗] LLM endpoint error: {response.text}")
            return False
    except Exception as e:
        print(f"[✗] Error testing LLM endpoint: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("Testing LLM with Google Maps Integration...\n")
    
    # Test Google Maps API
    maps_ok = test_maps_api()
    print()
    
    # Test Ollama API
    ollama_ok = test_ollama_api()
    print()
    
    # Test FastAPI server and LLM endpoint
    print("Note: The FastAPI server must be running for these tests")
    fastapi_ok = test_fastapi_server()
    llm_ok = test_llm_endpoint() if fastapi_ok else False
    print()
    
    # Summary
    print("Test Summary:")
    print(f"Google Maps API: {'✓' if maps_ok else '✗'}")
    print(f"Ollama API: {'✓' if ollama_ok else '✗'}")
    print(f"FastAPI Server: {'✓' if fastapi_ok else '✗'}")
    print(f"LLM Endpoint: {'✓' if llm_ok else '✗'}")
    
    if maps_ok and ollama_ok and fastapi_ok and llm_ok:
        print("\nAll tests passed! The application is working correctly.")
    else:
        print("\nSome tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()