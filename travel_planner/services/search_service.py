"""
Search service for handling flight and hotel searches using SerpAPI.
"""

import asyncio
from fastapi import HTTPException
from serpapi import GoogleSearch

from ..models import FlightRequest, HotelRequest
from ..config import SERP_API_KEY, logger
from ..constants import DEFAULT_FLIGHT_PARAMS, DEFAULT_HOTEL_PARAMS, SEARCH_ENGINES
from ..utils.location_utils import convert_airport_code_to_city, get_country_code_for_location, get_location_info


async def run_search(params: dict) -> dict:
    """
    Generic function to run SerpAPI searches asynchronously.
    
    Args:
        params: Dictionary of search parameters for SerpAPI
        
    Returns:
        Dictionary containing search results
        
    Raises:
        HTTPException: If the search API call fails
    """
    try:
        return await asyncio.to_thread(lambda: GoogleSearch(params).get_dict())
    except Exception as e:
        logger.exception(f"SerpAPI search error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Search API error: {str(e)}")


async def search_flights(flight_request: FlightRequest) -> list:
    """
    Fetch real-time flight details from Google Flights using SerpAPI.
    
    Args:
        flight_request: FlightRequest object containing search parameters
        
    Returns:
        List of flight data from SerpAPI
    """
    logger.info(f"Searching flights: {flight_request.origin} to {flight_request.destination}")

    # Build search parameters
    params = {
        "api_key": SERP_API_KEY,
        "engine": SEARCH_ENGINES["flights"],
        "departure_id": flight_request.origin.strip().upper(),
        "arrival_id": flight_request.destination.strip().upper(),
        "outbound_date": flight_request.outbound_date,
        "return_date": flight_request.return_date,
        **DEFAULT_FLIGHT_PARAMS
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


async def search_hotels(hotel_request: HotelRequest) -> list:
    """
    Fetch hotel information from SerpAPI with proper location handling.
    
    Args:
        hotel_request: HotelRequest object containing search parameters
        
    Returns:
        List of hotel data from SerpAPI
    """
    logger.info(f"Searching hotels for: {hotel_request.location}")

    # Get comprehensive location information
    location_info = get_location_info(hotel_request.location)
    
    logger.info(f"Location analysis: {location_info}")
    logger.info(f"Converted location query: {location_info['city_name']}")
    logger.info(f"Using country code: {location_info['country_code']}")
    logger.info(f"Is airport code: {location_info['is_airport_code']}")

    # Build search parameters with proper location and geographic bias
    params = {
        "api_key": SERP_API_KEY,
        "engine": SEARCH_ENGINES["hotels"],
        "q": location_info["city_name"],
        "gl": location_info["country_code"],
        "check_in_date": hotel_request.check_in_date,
        "check_out_date": hotel_request.check_out_date,
        **DEFAULT_HOTEL_PARAMS
    }

    search_results = await run_search(params)
    logger.info(f"SerpAPI hotel response keys: {list(search_results.keys()) if search_results else 'None'}")
    
    # Log the full response for debugging
    if search_results:
        logger.info(f"Full SerpAPI hotel response: {search_results}")
    
    hotels = search_results.get("properties", [])
    if hotels:
        logger.info(f"Found {len(hotels)} hotels")
        # Log the first hotel's structure for debugging
        if len(hotels) > 0:
            logger.info(f"First hotel structure: {hotels[0]}")
    else:
        logger.warning(f"No hotels found in response. Available keys: {list(search_results.keys()) if search_results else 'None'}")
    
    return hotels


def build_flight_search_params(flight_request: FlightRequest) -> dict:
    """
    Build search parameters for flight search.
    
    Args:
        flight_request: FlightRequest object
        
    Returns:
        Dictionary of search parameters
    """
    return {
        "api_key": SERP_API_KEY,
        "engine": SEARCH_ENGINES["flights"],
        "departure_id": flight_request.origin.strip().upper(),
        "arrival_id": flight_request.destination.strip().upper(),
        "outbound_date": flight_request.outbound_date,
        "return_date": flight_request.return_date,
        **DEFAULT_FLIGHT_PARAMS
    }


def build_hotel_search_params(hotel_request: HotelRequest) -> dict:
    """
    Build search parameters for hotel search with location conversion.
    
    Args:
        hotel_request: HotelRequest object
        
    Returns:
        Dictionary of search parameters
    """
    location_info = get_location_info(hotel_request.location)
    
    return {
        "api_key": SERP_API_KEY,
        "engine": SEARCH_ENGINES["hotels"],
        "q": location_info["city_name"],
        "gl": location_info["country_code"],
        "check_in_date": hotel_request.check_in_date,
        "check_out_date": hotel_request.check_out_date,
        **DEFAULT_HOTEL_PARAMS
    }
