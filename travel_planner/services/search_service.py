import asyncio
from fastapi import HTTPException
from serpapi import GoogleSearch
from ..models import FlightRequest, HotelRequest
from ..config import SERP_API_KEY, logger


async def run_search(params):
    """Generic function to run SerpAPI searches asynchronously."""
    try:
        return await asyncio.to_thread(lambda: GoogleSearch(params).get_dict())
    except Exception as e:
        logger.exception(f"SerpAPI search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search API error: {str(e)}")


async def search_flights(flight_request: FlightRequest):
    """Fetch real-time flight details from Google Flights using SerpAPI."""
    logger.info(f"Searching flights: {flight_request.origin} to {flight_request.destination}")

    params = {
        "api_key": SERP_API_KEY,
        "engine": "google_flights",
        "hl": "en",
        "gl": "us",
        "departure_id": flight_request.origin.strip().upper(),
        "arrival_id": flight_request.destination.strip().upper(),
        "outbound_date": flight_request.outbound_date,
        "return_date": flight_request.return_date,
        "currency": "USD"
    }

    search_results = await run_search(params)
    logger.info(f"SerpAPI response keys: {list(search_results.keys()) if search_results else 'None'}")
    
    # Log the full response for debugging
    if search_results:
        logger.info(f"Full SerpAPI response: {search_results}")
    
    # Extract flights from SerpAPI response structure
    flights = []
    if search_results:
        # Combine best_flights and other_flights
        best_flights = search_results.get("best_flights", [])
        other_flights = search_results.get("other_flights", [])
        
        # Combine all flights
        flights = best_flights + other_flights
        
        if flights:
            logger.info(f"Found {len(best_flights)} best flights and {len(other_flights)} other flights")
            logger.info(f"Total flights: {len(flights)}")
        else:
            logger.warning(f"No flights found in response. Available keys: {list(search_results.keys())}")
    
    return flights


async def search_hotels(hotel_request: HotelRequest):
    """Fetch hotel information from SerpAPI."""
    logger.info(f"Searching hotels for: {hotel_request.location}")

    params = {
        "api_key": SERP_API_KEY,
        "engine": "google_hotels",
        "q": hotel_request.location,
        "hl": "en",
        "gl": "us",
        "check_in_date": hotel_request.check_in_date,
        "check_out_date": hotel_request.check_out_date,
        "currency": "USD",
        "sort_by": 3,
        "rating": 8
    }

    search_results = await run_search(params)
    hotels = search_results.get("properties")
    return hotels
