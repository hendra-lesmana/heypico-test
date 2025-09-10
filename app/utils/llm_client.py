import os
import json
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv

# Try to import requests, but provide a mock if it's not available
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests package not available. LLM functionality will be limited.")

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost")
        self.port = os.getenv("OLLAMA_PORT", "11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3")
        self.api_url = f"{self.host}:{self.port}/api/generate"
        self.available = REQUESTS_AVAILABLE
    
    def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """Process a natural language prompt through the LLM to extract location information"""
        # Check if requests is available
        if not self.available:
            print("LLM functionality not available: requests package is missing")
            return self._fallback_response(prompt)
            
        # Enhance the prompt to extract location information
        system_prompt = """
        You are a helpful assistant that extracts location information from user queries. 
        If the user is asking about a place, extract the location name and any relevant details.
        If the user is asking for directions, extract the origin and destination locations.
        
        Format your response as JSON with the following structure:
        {{
            "response": "Your natural language response to the user",
            "location_query": "The location to search for (if applicable)",
            "directions_query": true/false,
            "origin": "Origin location for directions (if applicable)",
            "destination": "Destination location for directions (if applicable)",
            "travel_mode": "driving/walking/bicycling/transit (if applicable)"
        }}
        
        Only include fields that are relevant to the query.
        """
        
        enhanced_prompt = f"System: {system_prompt}\n\nUser: {prompt}\n\nAssistant:"
        
        try:
            # Call the Ollama API
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": enhanced_prompt,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                print(f"Error from Ollama API: {response.text}")
                return self._fallback_response(prompt)
            
            # Extract the response text
            result = response.json()
            response_text = result.get("response", "")
            
            # Try to parse JSON from the response
            try:
                # Find JSON in the response using regex
                json_match = re.search(r'\{[\s\S]*\}', response_text)
                if json_match:
                    json_str = json_match.group(0)
                    parsed_response = json.loads(json_str)
                    return parsed_response
                else:
                    # If no JSON found, use fallback
                    return self._fallback_response(prompt, response_text)
            except json.JSONDecodeError:
                # If JSON parsing fails, use fallback
                return self._fallback_response(prompt, response_text)
                
        except Exception as e:
            print(f"Error calling Ollama API: {str(e)}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str, llm_response: Optional[str] = None) -> Dict[str, Any]:
        """Generate a fallback response when LLM processing fails"""
        # Simple keyword-based extraction as fallback
        response = {}
        
        # Use LLM response if available, otherwise use a generic response
        if llm_response:
            response["response"] = llm_response
        else:
            response["response"] = f"I'll help you find information about {prompt}"
        
        # Check for direction-related keywords
        direction_keywords = ["direction", "directions", "how to get", "route to", "way to"]
        if any(keyword in prompt.lower() for keyword in direction_keywords):
            response["directions_query"] = True
            
            # Try to extract origin and destination
            from_match = re.search(r'from\s+([\w\s,]+)\s+to', prompt, re.IGNORECASE)
            to_match = re.search(r'to\s+([\w\s,]+)', prompt, re.IGNORECASE)
            
            if from_match:
                response["origin"] = from_match.group(1).strip()
            
            if to_match:
                response["destination"] = to_match.group(1).strip()
            
            # Check for travel mode
            if "walk" in prompt.lower() or "walking" in prompt.lower():
                response["travel_mode"] = "walking"
            elif "bike" in prompt.lower() or "cycling" in prompt.lower() or "bicycle" in prompt.lower():
                response["travel_mode"] = "bicycling"
            elif "transit" in prompt.lower() or "bus" in prompt.lower() or "train" in prompt.lower():
                response["travel_mode"] = "transit"
            else:
                response["travel_mode"] = "driving"
        else:
            # Assume it's a location search
            # Remove common question words and phrases
            clean_prompt = re.sub(r'^(where is|find|show me|locate|what is|tell me about)\s+', '', prompt, flags=re.IGNORECASE)
            response["location_query"] = clean_prompt
        
        return response