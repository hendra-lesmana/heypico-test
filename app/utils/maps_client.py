import os
import json
from dotenv import load_dotenv
from app.models.location import LocationResponse, DirectionsResponse, Place, Geometry, Route, Leg, Step
from typing import List, Dict, Any, Optional

# Try to import googlemaps, but provide a mock if it's not available
try:
    import googlemaps
    GOOGLEMAPS_AVAILABLE = True
except ImportError:
    GOOGLEMAPS_AVAILABLE = False
    print("Warning: googlemaps package not available. Map functionality will be limited.")

# Load environment variables
load_dotenv()

class MapsClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError("Google Maps API key not found in environment variables")
        self.available = GOOGLEMAPS_AVAILABLE
        
        if self.available:
            self.client = googlemaps.Client(key=self.api_key)
        else:
            self.client = None
    
    def search_place(self, query: str) -> LocationResponse:
        """Search for places based on a text query"""
        if not self.available:
            # Return mock data when googlemaps is not available
            return LocationResponse(
                places=[
                    Place(
                        place_id="mock-place-id",
                        name=f"Mock location for: {query}",
                        formatted_address="123 Mock Street, Mock City",
                        geometry=Geometry(lat=37.7749, lng=-122.4194),  # San Francisco coordinates
                        types=["point_of_interest"],
                        rating=4.5,
                        user_ratings_total=100,
                        photos=None
                    )
                ],
                status="OK"
            )
            
        try:
            # Use the Places API to search for the query
            places_result = self.client.places(query)
            
            # Process the results
            places = []
            for result in places_result.get("results", []):
                # Extract location data
                location = result.get("geometry", {}).get("location", {})
                
                # Create a Place object
                place = Place(
                    place_id=result.get("place_id", ""),
                    name=result.get("name", ""),
                    formatted_address=result.get("formatted_address", ""),
                    geometry=Geometry(
                        lat=location.get("lat", 0.0),
                        lng=location.get("lng", 0.0)
                    ),
                    types=result.get("types", []),
                    rating=result.get("rating"),
                    user_ratings_total=result.get("user_ratings_total"),
                    photos=result.get("photos")
                )
                places.append(place)
            
            return LocationResponse(
                places=places,
                status=places_result.get("status", "UNKNOWN")
            )
        except Exception as e:
            # Log the error and return an empty response
            print(f"Error searching for place: {str(e)}")
            return LocationResponse(places=[], status="ERROR")
    
    def get_directions(self, origin: str, destination: str, mode: str = "driving") -> DirectionsResponse:
        """Get directions from origin to destination"""
        if not self.available:
            # Return mock data when googlemaps is not available
            mock_step = Step(
                distance={"text": "5 mi", "value": 8000},
                duration={"text": "10 mins", "value": 600},
                html_instructions="Head <b>north</b> on <b>Mock Street</b>",
                polyline={"points": "mock_polyline_string"},
                start_location=Geometry(lat=37.7749, lng=-122.4194),
                end_location=Geometry(lat=37.8049, lng=-122.4194),
                travel_mode=mode.upper()
            )
            
            mock_leg = Leg(
                distance={"text": "10 mi", "value": 16000},
                duration={"text": "20 mins", "value": 1200},
                start_address=f"Mock origin: {origin}",
                end_address=f"Mock destination: {destination}",
                start_location=Geometry(lat=37.7749, lng=-122.4194),
                end_location=Geometry(lat=37.8349, lng=-122.4194),
                steps=[mock_step]
            )
            
            mock_route = Route(
                summary=f"Mock route from {origin} to {destination}",
                legs=[mock_leg],
                overview_polyline={"points": "mock_overview_polyline_string"},
                warnings=[],
                bounds={"northeast": {"lat": 37.8349, "lng": -122.4094}, "southwest": {"lat": 37.7749, "lng": -122.4294}},
                copyrights="Mock Map Data"
            )
            
            return DirectionsResponse(
                routes=[mock_route],
                status="OK"
            )
            
        try:
            # Use the Directions API
            directions_result = self.client.directions(
                origin=origin,
                destination=destination,
                mode=mode
            )
            
            # Process the results
            routes = []
            for route_data in directions_result:
                legs = []
                for leg_data in route_data.get("legs", []):
                    steps = []
                    for step_data in leg_data.get("steps", []):
                        step = Step(
                            distance=step_data.get("distance", {}),
                            duration=step_data.get("duration", {}),
                            html_instructions=step_data.get("html_instructions", ""),
                            polyline=step_data.get("polyline", {}),
                            start_location=Geometry(
                                lat=step_data.get("start_location", {}).get("lat", 0.0),
                                lng=step_data.get("start_location", {}).get("lng", 0.0)
                            ),
                            end_location=Geometry(
                                lat=step_data.get("end_location", {}).get("lat", 0.0),
                                lng=step_data.get("end_location", {}).get("lng", 0.0)
                            ),
                            travel_mode=step_data.get("travel_mode", "")
                        )
                        steps.append(step)
                    
                    leg = Leg(
                        distance=leg_data.get("distance", {}),
                        duration=leg_data.get("duration", {}),
                        start_address=leg_data.get("start_address", ""),
                        end_address=leg_data.get("end_address", ""),
                        start_location=Geometry(
                            lat=leg_data.get("start_location", {}).get("lat", 0.0),
                            lng=leg_data.get("start_location", {}).get("lng", 0.0)
                        ),
                        end_location=Geometry(
                            lat=leg_data.get("end_location", {}).get("lat", 0.0),
                            lng=leg_data.get("end_location", {}).get("lng", 0.0)
                        ),
                        steps=steps
                    )
                    legs.append(leg)
                
                route = Route(
                    summary=route_data.get("summary", ""),
                    legs=legs,
                    overview_polyline=route_data.get("overview_polyline", {}),
                    warnings=route_data.get("warnings", []),
                    bounds=route_data.get("bounds", {}),
                    copyrights=route_data.get("copyrights", "")
                )
                routes.append(route)
            
            return DirectionsResponse(
                routes=routes,
                status="OK" if routes else "ZERO_RESULTS"
            )
        except Exception as e:
            # Log the error and return an empty response
            print(f"Error getting directions: {str(e)}")
            return DirectionsResponse(routes=[], status="ERROR")
    
    def generate_map_html(self, place: Place) -> str:
        """Generate HTML for embedding a Google Map with a marker for the place"""
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        lat = place.geometry.lat
        lng = place.geometry.lng
        name = place.name.replace("'", "\\'")  # Escape single quotes
        
        if not self.available:
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{name} - Map</title>
                <style>
                    #map {{height: 400px; width: 100%; display: flex; align-items: center; justify-content: center; background-color: #f0f0f0;}}
                    body {{margin: 0; padding: 0; font-family: Arial, sans-serif;}}
                </style>
            </head>
            <body>
                <div id="map">
                    <div style="text-align: center; padding: 20px;">
                        <h3>Map Preview Unavailable</h3>
                        <p>Google Maps API is not available. Please install the googlemaps package.</p>
                        <p>Location: {name}</p>
                        <p>Address: {place.formatted_address}</p>
                        <p>Coordinates: Latitude {lat}, Longitude {lng}</p>
                    </div>
                </div>
            </body>
            </html>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{name} - Map</title>
            <style>
                #map {{height: 400px; width: 100%;}}
                body {{margin: 0; padding: 0; font-family: Arial, sans-serif;}}
                .info-window {{padding: 10px;}}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                function initMap() {{
                    const location = {{lat: {lat}, lng: {lng}}};
                    const map = new google.maps.Map(document.getElementById('map'), {{
                        zoom: 15,
                        center: location
                    }});
                    
                    const marker = new google.maps.Marker({{
                        position: location,
                        map: map,
                        title: '{name}'
                    }});
                    
                    const infoWindow = new google.maps.InfoWindow({{
                        content: '<div class="info-window"><h3>{name}</h3><p>{place.formatted_address}</p></div>'
                    }});
                    
                    marker.addListener('click', () => {{
                        infoWindow.open(map, marker);
                    }});
                    
                    // Open info window by default
                    infoWindow.open(map, marker);
                }}
            </script>
            <script async defer src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap"></script>
        </body>
        </html>
        """
        
        return html
    
    def generate_directions_map_html(self, directions: DirectionsResponse) -> str:
        """Generate HTML for embedding a Google Map with directions"""
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        
        if not directions.routes or not directions.routes[0].legs:
            return "<p>No directions available</p>"
        
        route = directions.routes[0]
        leg = route.legs[0]
        
        # Extract start and end points
        start_lat = leg.start_location.lat
        start_lng = leg.start_location.lng
        end_lat = leg.end_location.lat
        end_lng = leg.end_location.lng
        
        # Extract polyline for the route
        polyline = route.overview_polyline.get("points", "")
        
        # Create steps HTML
        steps_html = ""
        for i, step in enumerate(leg.steps):
            steps_html += f"""
            <div class="direction-step">
                <span class="step-number">{i+1}.</span>
                <span class="step-instruction">{step.html_instructions}</span>
                <span class="step-distance">{step.distance.get('text', '')}</span>
            </div>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Directions Map</title>
            <style>
                #map {{height: 400px; width: 100%;}}
                body {{margin: 0; padding: 0; font-family: Arial, sans-serif;}}
                .directions-container {{padding: 15px;}}
                .direction-step {{margin-bottom: 10px; padding: 5px; border-bottom: 1px solid #eee;}}
                .step-number {{font-weight: bold; margin-right: 10px;}}
                .step-distance {{color: #666; margin-left: 10px;}}
                .route-summary {{font-weight: bold; margin-bottom: 15px;}}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <div class="directions-container">
                <div class="route-summary">
                    <p>From: {leg.start_address}</p>
                    <p>To: {leg.end_address}</p>
                    <p>Distance: {leg.distance.get('text', '')}, Duration: {leg.duration.get('text', '')}</p>
                </div>
                <h3>Directions:</h3>
                <div class="steps-container">
                    {steps_html}
                </div>
            </div>
            <script>
                function initMap() {{
                    const directionsService = new google.maps.DirectionsService();
                    const directionsRenderer = new google.maps.DirectionsRenderer();
                    
                    const map = new google.maps.Map(document.getElementById('map'), {{
                        zoom: 7,
                        center: {{lat: {start_lat}, lng: {start_lng}}}
                    }});
                    
                    directionsRenderer.setMap(map);
                    
                    const request = {{
                        origin: {{lat: {start_lat}, lng: {start_lng}}},
                        destination: {{lat: {end_lat}, lng: {end_lng}}},
                        travelMode: '{leg.steps[0].travel_mode if leg.steps else "DRIVING"}'
                    }};
                    
                    directionsService.route(request, (result, status) => {{
                        if (status === 'OK') {{
                            directionsRenderer.setDirections(result);
                        }}
                    }});
                }}
            </script>
            <script async defer src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap"></script>
        </body>
        </html>
        """
        
        return html