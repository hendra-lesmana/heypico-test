from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from app.models.location import LocationResponse, DirectionsResponse
from app.utils.maps_client import MapsClient
from app.utils.llm_client import LLMClient

router = APIRouter()
maps_client = MapsClient()
llm_client = LLMClient()

class LocationQuery(BaseModel):
    query: str

@router.post("/search", response_model=LocationResponse)
async def search_location(query: LocationQuery):
    """Search for a location based on a query string"""
    try:
        result = maps_client.search_place(query.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/directions", response_model=DirectionsResponse)
async def get_directions(
    origin: str = Query(..., description="Origin address or coordinates"),
    destination: str = Query(..., description="Destination address or coordinates"),
    mode: str = Query("driving", description="Travel mode: driving, walking, bicycling, transit")
):
    """Get directions from origin to destination"""
    try:
        result = maps_client.get_directions(origin, destination, mode)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class LLMRequest(BaseModel):
    prompt: str

class LLMResponse(BaseModel):
    text: str
    locations: Optional[List[LocationResponse]] = None
    directions: Optional[DirectionsResponse] = None
    map_html: Optional[str] = None
    web_url: Optional[str] = None

@router.post("/llm", response_model=LLMResponse)
async def process_llm_request(request: LLMRequest):
    """Process a natural language request through the LLM and return relevant map data"""
    try:
        # Process the prompt with LLM to extract location information
        llm_result = llm_client.process_prompt(request.prompt)
        
        # If locations were identified, search for them
        locations = None
        directions = None
        map_html = None
        web_url = None
        
        if llm_result.get("location_query"):
            try:
                location_response = maps_client.search_place(llm_result["location_query"])
                
                # Check if we have a web fallback
                if location_response and location_response.status == "WEB_FALLBACK":
                    web_url = location_response.web_url
                    # Don't generate map HTML for web fallback
                    map_html = None
                    locations = [location_response]  # Wrap in list
                elif location_response and location_response.places:
                    # Generate map HTML for regular locations
                    map_html = maps_client.generate_map_html(location_response.places[0])
                    locations = [location_response]  # Wrap in list
            except Exception as e:
                print(f"Error processing location query: {str(e)}")
                # Return the web fallback response when API fails
                location_response = maps_client.search_place(llm_result["location_query"])
                locations = [location_response]  # Wrap in list
        
        # If directions were requested, get them
        if llm_result.get("directions_query"):
            origin = llm_result.get("origin", "")
            destination = llm_result.get("destination", "")
            mode = llm_result.get("travel_mode", "driving")
            
            if origin and destination:
                directions = maps_client.get_directions(origin, destination, mode)
                
                # Generate directions map
                if directions and directions.routes:
                    map_html = maps_client.generate_directions_map_html(directions)
        
        return LLMResponse(
            text=llm_result.get("response", ""),
            locations=locations,
            directions=directions,
            map_html=map_html,
            web_url=web_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))