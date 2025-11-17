from typing import List, Dict, Any
from ..models import FlightInfo, HotelInfo


def transform_serpapi_flights(raw_flights: List[Dict[str, Any]]) -> List[FlightInfo]:
    """Transform raw SerpAPI flight data to FlightInfo models."""
    if not raw_flights:
        return []
    
    transformed_flights = []
    for flight_data in raw_flights:
        # Extract flight details - SerpAPI returns complex nested structure
        flights_list = flight_data.get("flights", [])
        total_duration = flight_data.get("total_duration", 0)
        price = flight_data.get("price", 0)
        layovers = flight_data.get("layovers", [])
        
        # Get primary airline from first flight segment
        primary_flight = flights_list[0] if flights_list else {}
        
        # Calculate stops from layovers
        stops_count = len(layovers)
        stops_text = f"{stops_count} stop{'s' if stops_count != 1 else ''}" if stops_count > 0 else "Direct"
        
        # Get departure and arrival info from first and last flight segments
        departure_info = primary_flight.get("departure_airport", {})
        arrival_info = flights_list[-1].get("arrival_airport", {}) if flights_list else {}
        
        # Convert duration from minutes to readable format
        hours = total_duration // 60
        minutes = total_duration % 60
        duration_text = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
        
        # Map SerpAPI fields to our FlightInfo model
        flight_info = FlightInfo(
            airline=primary_flight.get("airline", "Multiple Airlines"),
            price=f"${price}" if price else "N/A",
            duration=duration_text,
            stops=stops_text,
            departure=departure_info.get("time", "N/A"),
            arrival=arrival_info.get("time", "N/A"),
            travel_class=primary_flight.get("travel_class", "Economy"),
            return_date=flight_data.get("return_date", "N/A"),
            airline_logo=flight_data.get("airline_logo", primary_flight.get("airline_logo", ""))
        )
        transformed_flights.append(flight_info)
    
    return transformed_flights


def transform_serpapi_hotels(raw_hotels: List[Dict[str, Any]]) -> List[HotelInfo]:
    """Transform raw SerpAPI hotel data to HotelInfo models."""
    if not raw_hotels:
        return []
    
    transformed_hotels = []
    for hotel_data in raw_hotels:
        # Map SerpAPI fields to our HotelInfo model
        hotel_info = HotelInfo(
            name=hotel_data.get("name", "Unknown Hotel"),
            price=str(hotel_data.get("rate_per_night", {}).get("lowest", "N/A")),
            rating=float(hotel_data.get("overall_rating", 0.0)),
            location=hotel_data.get("neighborhood", "N/A"),
            link=hotel_data.get("link", "")
        )
        transformed_hotels.append(hotel_info)
    
    return transformed_hotels
