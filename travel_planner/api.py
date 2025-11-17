import uvicorn
from fastapi import FastAPI, HTTPException
from .models import FlightRequest, HotelRequest, ItineraryRequest, AIResponse
from .services.search_service import search_flights, search_hotels
from .services.ai_service import get_ai_recommendation, generate_itinerary
from .utils.formatters import format_travel_data
from .utils.transformers import transform_serpapi_flights, transform_serpapi_hotels
from .config import logger

app = FastAPI(title="Travel Planning API", version="1.0.1")


@app.post("/search_flights/", response_model=AIResponse)
async def get_flight_recommendations(flight_request: FlightRequest):
    raw_flights = await search_flights(flight_request)
    # Transform raw SerpAPI data to FlightInfo models
    flights = transform_serpapi_flights(raw_flights if raw_flights else [])
    flights_text = format_travel_data("flights", raw_flights if raw_flights else [])
    ai_recommendation = await get_ai_recommendation("flights", flights_text)
    return AIResponse(flights=flights, ai_flight_recommendation=ai_recommendation)


@app.post("/search_hotels/", response_model=AIResponse)
async def get_hotel_recommendations(hotel_request: HotelRequest):
    raw_hotels = await search_hotels(hotel_request)
    # Transform raw SerpAPI data to HotelInfo models
    hotels = transform_serpapi_hotels(raw_hotels if raw_hotels else [])
    hotels_text = format_travel_data("hotels", raw_hotels if raw_hotels else [])
    ai_recommendation = await get_ai_recommendation("hotels", hotels_text)
    return AIResponse(hotels=hotels, ai_hotel_recommendation=ai_recommendation)


@app.post("/generate_itinerary/", response_model=AIResponse)
async def get_itinerary(itinerary_request: ItineraryRequest):
    itinerary = await generate_itinerary(
        itinerary_request.destination,
        itinerary_request.flights,
        itinerary_request.hotels,
        itinerary_request.check_in_date,
        itinerary_request.check_out_date
    )
    return AIResponse(itinerary=itinerary)


# Run FastAPI Server
if __name__ == "__main__":
    logger.info("Starting Travel Planning API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
