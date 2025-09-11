#!/usr/bin/env python3
import requests
import json

# Test the web fallback functionality
def test_web_fallback():
    print("Testing web fallback functionality...")
    
    # Test the LLM endpoint
    test_prompt = "Where is the Eiffel Tower"
    
    try:
        response = requests.post(
            "http://localhost:8000/api/llm",
            json={"prompt": test_prompt},
            timeout=10
        )
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if data.get("web_url"):
                print(f"✅ Web URL found: {data['web_url']}")
                return True
            else:
                print("❌ No web URL in response")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_web_fallback()