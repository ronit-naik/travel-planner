def format_travel_data(data_type, data):
    """Format travel data for AI analysis."""
    if not data:
        return f"No {data_type} data available."
    
    if data_type == "flights":
        return format_flight_data(data)
    elif data_type == "hotels":
        return format_hotel_data(data)
    else:
        return str(data)


def format_flight_data(flights):
    """Format flight data for AI analysis."""
    if not flights:
        return "No flight data available."
    
    formatted_flights = []
    for i, flight in enumerate(flights, 1):
        flight_info = f"""
Flight {i}:
- Airline: {flight.get('airline', 'N/A')}
- Price: {flight.get('price', 'N/A')}
- Duration: {flight.get('duration', 'N/A')}
- Stops: {flight.get('stops', 'N/A')}
- Departure: {flight.get('departure', 'N/A')}
- Arrival: {flight.get('arrival', 'N/A')}
- Travel Class: {flight.get('travel_class', 'N/A')}
"""
        formatted_flights.append(flight_info)
    
    return "\n".join(formatted_flights)


def format_hotel_data(hotels):
    """Format hotel data for AI analysis."""
    if not hotels:
        return "No hotel data available."
    
    formatted_hotels = []
    for i, hotel in enumerate(hotels, 1):
        hotel_info = f"""
Hotel {i}:
- Name: {hotel.get('name', 'N/A')}
- Price: {hotel.get('price', 'N/A')}
- Rating: {hotel.get('rating', 'N/A')}
- Location: {hotel.get('location', 'N/A')}
- Link: {hotel.get('link', 'N/A')}
"""
        formatted_hotels.append(hotel_info)
    
    return "\n".join(formatted_hotels)
