#!/usr/bin/env python3
import requests
import json

def test_web_fallback():
    """Test the web fallback functionality comprehensively"""
    
    print("🧪 Testing Web Fallback Functionality")
    print("=" * 50)
    
    test_prompts = [
        "Where is the Eiffel Tower",
        "Find restaurants near me",
        "Show me Times Square"
    ]
    
    all_passed = True
    
    for prompt in test_prompts:
        print(f"\n📍 Testing: {prompt}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/llm",
                json={"prompt": prompt},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if web_url is present
                if data.get("web_url"):
                    print(f"   ✅ Web URL found: {data['web_url']}")
                    
                    # Check if it's a Google Maps URL
                    if "google.com/maps/search" in data['web_url']:
                        print(f"   ✅ Valid Google Maps URL")
                    else:
                        print(f"   ❌ Invalid URL format")
                        all_passed = False
                else:
                    print(f"   ❌ No web URL in response")
                    all_passed = False
                
                # Check if locations array contains the web fallback
                if data.get("locations") and len(data["locations"]) > 0:
                    location = data["locations"][0]
                    if location.get("status") == "WEB_FALLBACK":
                        print(f"   ✅ WEB_FALLBACK status detected")
                    else:
                        print(f"   ❌ Missing WEB_FALLBACK status")
                        all_passed = False
                else:
                    print(f"   ❌ No locations data")
                    all_passed = False
                    
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests PASSED! Web fallback is working correctly.")
    else:
        print("❌ Some tests FAILED. Please check the implementation.")
    
    return all_passed

if __name__ == "__main__":
    test_web_fallback()