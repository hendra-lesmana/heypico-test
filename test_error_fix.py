import requests
import json

def test_empty_location_query():
    """Test the fix for the 500 Internal Server Error with an empty location query"""
    print("Testing empty location query handling...")
    
    # This prompt would previously cause a 500 error due to empty location_query after cleaning
    response = requests.post(
        "http://localhost:8000/api/llm",
        json={"prompt": "how do i go to bandung from jakarta"}
    )
    
    print(f"Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("Response successful!")
        print(f"Response data: {json.dumps(data, indent=2)}")
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    print("Testing fix for 500 Internal Server Error...\n")
    success = test_empty_location_query()
    
    if success:
        print("\nTest passed successfully! The 500 Internal Server Error has been fixed.")
    else:
        print("\nTest failed. The issue may not be fully resolved.")