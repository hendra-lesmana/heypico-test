#!/usr/bin/env python3
"""
Test script to verify web fallback functionality when Google Maps API is unavailable
"""

import requests
import json

def test_web_fallback():
    """Test that web URLs are provided when Google Maps API fails"""
    
    test_prompts = [
        "Where is the Eiffel Tower",
        "Find restaurants near me",
        "Show me Times Square"
    ]
    
    api_url = "http://localhost:8000/api/llm"
    
    print("Testing web fallback functionality...")
    print("=" * 50)
    
    for prompt in test_prompts:
        print(f"\nTesting prompt: '{prompt}'")
        
        try:
            response = requests.post(api_url, json={"prompt": prompt})
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"Response: {data.get('text', 'No response')}")
                
                if data.get('web_url'):
                    print(f"✅ Web fallback URL: {data['web_url']}")
                    
                    # Verify the URL format
                    expected_url = f"https://www.google.com/maps/search/{prompt.replace(' ', '+')}"
                    if data['web_url'] == expected_url:
                        print("✅ URL format is correct")
                    else:
                        print(f"⚠️ URL format differs: {data['web_url']}")
                else:
                    print("❌ No web URL provided")
                    
                if data.get('locations'):
                    locations = data['locations']
                    print(f"📍 Found {len(locations.get('places', []))} locations")
                    if locations.get('status') == 'WEB_FALLBACK':
                        print("✅ Status indicates web fallback")
                else:
                    print("📍 No locations data")
                    
            else:
                print(f"❌ API request failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Web fallback test completed!")

if __name__ == "__main__":
    test_web_fallback()