from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Geometry(BaseModel):
    lat: float
    lng: float

class Place(BaseModel):
    place_id: str
    name: str
    formatted_address: str
    geometry: Geometry
    types: List[str] = []
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    photos: Optional[List[Dict[str, Any]]] = None
    opening_hours: Optional[Dict[str, Any]] = None
    website: Optional[str] = None
    international_phone_number: Optional[str] = None

class LocationResponse(BaseModel):
    places: List[Place] = []
    status: str
    web_url: Optional[str] = None

class Step(BaseModel):
    distance: Dict[str, Any]
    duration: Dict[str, Any]
    html_instructions: str
    polyline: Dict[str, Any]
    start_location: Geometry
    end_location: Geometry
    travel_mode: str

class Leg(BaseModel):
    distance: Dict[str, Any]
    duration: Dict[str, Any]
    start_address: str
    end_address: str
    start_location: Geometry
    end_location: Geometry
    steps: List[Step]

class Route(BaseModel):
    summary: str
    legs: List[Leg]
    overview_polyline: Dict[str, Any]
    warnings: List[str] = []
    bounds: Dict[str, Any]
    copyrights: str

class DirectionsResponse(BaseModel):
    routes: List[Route] = []
    status: str