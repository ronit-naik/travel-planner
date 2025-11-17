import streamlit as st
import requests
from datetime import datetime, timedelta
import json

# API URLs
API_BASE_URL = "http://localhost:8000"
API_URL_FLIGHTS = f"{API_BASE_URL}/search_flights/"
API_URL_HOTELS = f"{API_BASE_URL}/search_hotels/"
API_URL_ITINERARY = f"{API_BASE_URL}/generate_itinerary/"

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Main title
st.title("✈️ AI Travel Planner")
st.markdown("Plan your perfect trip with AI-powered recommendations!")

# Helper function to make API calls
def make_api_call(url, data):
    try:
        response = requests.post(url, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return None

# Initialize session state for storing search results
if 'flight_results' not in st.session_state:
    st.session_state.flight_results = None
if 'hotel_results' not in st.session_state:
    st.session_state.hotel_results = None
if 'itinerary_results' not in st.session_state:
    st.session_state.itinerary_results = None

# Create two columns for flight and hotel search
col1, col2 = st.columns(2)

with col1:
    st.subheader("🛫 Flight Search")
    
    departure_airport = st.text_input("From (Airport Code)", placeholder="e.g., HYD", key="dep_airport")
    arrival_airport = st.text_input("To (Airport Code)", placeholder="e.g., SYD", key="arr_airport")
    departure_date = st.date_input("Departure Date", min_value=datetime.now().date(), key="dep_date")
    return_date = st.date_input("Return Date", min_value=datetime.now().date() + timedelta(days=1), key="ret_date")
    
    if st.button("Search Flights", type="primary", key="search_flights"):
        if departure_airport and arrival_airport:
            with st.spinner("Searching for flights..."):
                flight_data = {
                    "origin": departure_airport.upper(),
                    "destination": arrival_airport.upper(),
                    "outbound_date": departure_date.strftime("%Y-%m-%d"),
                    "return_date": return_date.strftime("%Y-%m-%d")
                }
                
                result = make_api_call(API_URL_FLIGHTS, flight_data)
                if result:
                    st.session_state.flight_results = result
                    st.success("Flight search completed!")
        else:
            st.error("Please fill in both departure and arrival airports.")

with col2:
    st.subheader("🏨 Hotel Search")
    
    # Option to use flight destination for hotel search
    use_flight_destination = st.checkbox("Use flight destination for hotel", key="use_flight_dest")
    
    if use_flight_destination and arrival_airport:
        hotel_location = arrival_airport.upper()
        st.info(f"Using flight destination: {hotel_location}")
    else:
        hotel_location = st.text_input("Location", placeholder="e.g., SYD", key="hotel_location")
    
    check_in_date = st.date_input("Check-in Date", min_value=datetime.now().date(), key="checkin_date")
    check_out_date = st.date_input("Check-out Date", min_value=datetime.now().date() + timedelta(days=1), key="checkout_date")
    
    if st.button("Search Hotels", type="primary", key="search_hotels"):
        location_to_use = hotel_location if not use_flight_destination else arrival_airport.upper()
        if location_to_use:
            with st.spinner("Searching for hotels..."):
                hotel_data = {
                    "location": location_to_use,
                    "check_in_date": check_in_date.strftime("%Y-%m-%d"),
                    "check_out_date": check_out_date.strftime("%Y-%m-%d")
                }
                
                result = make_api_call(API_URL_HOTELS, hotel_data)
                if result:
                    st.session_state.hotel_results = result
                    st.success("Hotel search completed!")
        else:
            st.error("Please enter a location.")

# Tab navigation
tab1, tab2, tab3, tab4 = st.tabs(["✈️ Flights", "🏨 Hotels", "🤖 AI Recommendations", "📅 Itinerary"])

with tab1:
    if st.session_state.flight_results and st.session_state.flight_results.get("flights"):
        st.subheader(f"✈️ Available Flights from {departure_airport.upper() if departure_airport else 'Origin'} to {arrival_airport.upper() if arrival_airport else 'Destination'}")
        
        flights = st.session_state.flight_results["flights"]
        
        # Display flights in a grid layout using Streamlit columns
        for i in range(0, len(flights), 2):
            cols = st.columns(2)
            
            for j, col in enumerate(cols):
                if i + j < len(flights):
                    flight = flights[i + j]
                    
                    with col:
                        # Create a flight card using Streamlit components with custom styling
                        with st.container():
                            # Add custom CSS for this specific card
                            st.markdown(f"""
                            <style>
                            .flight-card-{i+j} {{
                                border: 1px solid #ddd;
                                border-radius: 8px;
                                padding: 1rem;
                                margin: 0.5rem 0;
                                background: var(--background-color);
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            }}
                            .price-tag-{i+j} {{
                                background: #ff6b35;
                                color: white;
                                padding: 0.25rem 0.75rem;
                                border-radius: 4px;
                                font-weight: bold;
                                display: inline-block;
                            }}
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # Flight header
                            header_col1, header_col2 = st.columns([3, 1])
                            with header_col1:
                                st.markdown(f"**✈️ {flight.get('airline', 'Unknown Airline')}**")
                            with header_col2:
                                st.markdown(f'<span class="price-tag-{i+j}">{flight.get("price", "N/A")}</span>', unsafe_allow_html=True)
                            
                            # Flight details
                            detail_col1, detail_col2 = st.columns(2)
                            with detail_col1:
                                st.markdown(f"**Departure:** {flight.get('departure', 'N/A')}")
                                st.markdown(f"**Duration:** {flight.get('duration', 'N/A')}")
                            with detail_col2:
                                st.markdown(f"**Arrival:** {flight.get('arrival', 'N/A')}")
                                st.markdown(f"**Stops:** {flight.get('stops', 'N/A')}")
                            
                            st.markdown(f"**Class:** {flight.get('travel_class', 'Economy')}")
                            st.divider()
    else:
        st.info("Search for flights to see available options here.")

with tab2:
    if st.session_state.hotel_results and st.session_state.hotel_results.get("hotels"):
        location_display = hotel_location if not use_flight_destination else arrival_airport.upper()
        st.subheader(f"🏨 Available Hotels in {location_display if location_display else 'Location'}")
        
        hotels = st.session_state.hotel_results["hotels"]
        
        # Display hotels in a grid layout
        for i in range(0, len(hotels), 3):
            cols = st.columns(3)
            
            for j, col in enumerate(cols):
                if i + j < len(hotels):
                    hotel = hotels[i + j]
                    
                    with col:
                        # Create a hotel card using Streamlit components with custom styling
                        with st.container():
                            # Add custom CSS for this specific hotel card
                            st.markdown(f"""
                            <style>
                            .hotel-card-{i+j} {{
                                border: 1px solid #ddd;
                                border-radius: 8px;
                                padding: 1rem;
                                margin: 0.5rem 0;
                                background: var(--background-color);
                                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            }}
                            .hotel-price-tag-{i+j} {{
                                background: #ff6b35;
                                color: white;
                                padding: 0.25rem 0.5rem;
                                border-radius: 4px;
                                font-weight: bold;
                                font-size: 0.9rem;
                                display: inline-block;
                            }}
                            </style>
                            """, unsafe_allow_html=True)
                            
                            # Hotel header
                            st.markdown(f"**🏨 {hotel.get('name', 'Unknown Hotel')}**")
                            
                            # Price tag
                            st.markdown(f'<span class="hotel-price-tag-{i+j}">{hotel.get("price", "N/A")} per night</span>', unsafe_allow_html=True)
                            
                            # Hotel details
                            st.markdown(f"**⭐ Rating:** {hotel.get('rating', 'N/A')}")
                            st.markdown(f"**📍 Location:** {hotel.get('location', 'N/A')}")
                            
                            # Action buttons using Streamlit components
                            button_col1, button_col2 = st.columns(2)
                            with button_col1:
                                if st.button("✏️ Select", key=f"select_hotel_{i+j}"):
                                    # Add hotel to selected list in session state
                                    if 'selected_hotels' not in st.session_state:
                                        st.session_state.selected_hotels = []
                                    
                                    hotel_id = f"hotel_{i+j}"
                                    if hotel_id not in st.session_state.selected_hotels:
                                        st.session_state.selected_hotels.append(hotel_id)
                                        st.success(f"Selected: {hotel.get('name', 'Hotel')}")
                                    else:
                                        st.info("Hotel already selected!")
                                        
                            with button_col2:
                                if st.button("📋 Details", key=f"details_hotel_{i+j}"):
                                    # Show hotel details in an expander
                                    with st.expander(f"Details for {hotel.get('name', 'Hotel')}", expanded=True):
                                        st.write(f"**🏨 Hotel Name:** {hotel.get('name', 'Unknown Hotel')}")
                                        st.write(f"**💰 Price:** {hotel.get('price', 'N/A')}")
                                        st.write(f"**⭐ Rating:** {hotel.get('rating', 'N/A')}/5.0")
                                        st.write(f"**📍 Location:** {hotel.get('location', 'N/A')}")
                                        if hotel.get('link'):
                                            st.write(f"**🔗 Hotel Link:** [View on Google]({hotel.get('link')})")
                                        else:
                                            st.write("**🔗 Hotel Link:** Not available")
                            
                            st.divider()
    else:
        st.info("Search for hotels to see available options here.")

with tab3:
    st.subheader("🤖 AI Recommendations")
    
    # Display AI recommendations for flights
    if st.session_state.flight_results and st.session_state.flight_results.get("ai_flight_recommendation"):
        st.markdown("### ✈️ Flight Recommendations")
        st.markdown(st.session_state.flight_results["ai_flight_recommendation"])
    
    # Display AI recommendations for hotels
    if st.session_state.hotel_results and st.session_state.hotel_results.get("ai_hotel_recommendation"):
        st.markdown("### 🏨 Hotel Recommendations")
        st.markdown(st.session_state.hotel_results["ai_hotel_recommendation"])
    
    if not (st.session_state.flight_results or st.session_state.hotel_results):
        st.info("Search for flights or hotels to get AI-powered recommendations!")

with tab4:
    st.subheader("📅 Your Travel Itinerary")
    
    # Itinerary generation form
    if st.session_state.flight_results or st.session_state.hotel_results:
        destination = st.text_input("Destination", placeholder="e.g., Sydney, Paris", key="itinerary_dest")
        
        col1, col2 = st.columns(2)
        with col1:
            trip_start = st.date_input("Trip Start Date", min_value=datetime.now().date(), key="trip_start")
        with col2:
            trip_end = st.date_input("Trip End Date", min_value=datetime.now().date() + timedelta(days=1), key="trip_end")
        
        # Pre-fill with search results if available
        flight_info = "Flight information from search results" if st.session_state.flight_results else ""
        hotel_info = "Hotel information from search results" if st.session_state.hotel_results else ""
        
        flights_info = st.text_area("Flight Information", value=flight_info, key="itinerary_flights")
        hotels_info = st.text_area("Hotel Information", value=hotel_info, key="itinerary_hotels")
        
        if st.button("Generate Itinerary", type="primary", key="generate_itinerary"):
            if destination and flights_info and hotels_info:
                with st.spinner("Generating your personalized itinerary..."):
                    itinerary_data = {
                        "destination": destination,
                        "check_in_date": trip_start.strftime("%Y-%m-%d"),
                        "check_out_date": trip_end.strftime("%Y-%m-%d"),
                        "flights": flights_info,
                        "hotels": hotels_info
                    }
                    
                    result = make_api_call(API_URL_ITINERARY, itinerary_data)
                    if result:
                        st.session_state.itinerary_results = result
                        st.success("Itinerary generated successfully!")
            else:
                st.error("Please fill in all required fields.")
    
    # Display generated itinerary
    if st.session_state.itinerary_results and st.session_state.itinerary_results.get("itinerary"):
        st.markdown("### 📋 Your Personalized Itinerary")
        st.markdown(st.session_state.itinerary_results["itinerary"])
    elif not (st.session_state.flight_results or st.session_state.hotel_results):
        st.info("Search for flights and hotels first to generate a personalized itinerary!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    Made with ❤️ using Streamlit and FastAPI
</div>
""", unsafe_allow_html=True)
