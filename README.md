# ✈️ AI Travel Planner

An intelligent travel planning application that helps users find the best flights, hotels, and generate personalized itineraries using AI recommendations.

## 🌟 Features

- **Flight Search**: Search for flights between airports with date flexibility
- **Hotel Search**: Find accommodations with check-in/check-out dates
- **AI Recommendations**: Get intelligent suggestions powered by Gemini AI
- **Itinerary Generation**: Create detailed travel itineraries
- **Interactive UI**: User-friendly Streamlit web interface
- **REST API**: FastAPI backend with comprehensive endpoints

## 🏗️ Architecture

- **Backend**: FastAPI with Python 3.8+
- **Frontend**: Streamlit web application
- **AI Engine**: Google Gemini 2.0 Flash via CrewAI
- **Data Sources**: SerpAPI for real-time flight and hotel data
- **Data Validation**: Pydantic models

## 📁 Project Structure

```
travel_planner/
├── main.py                     # Main entry point
├── travel_planner/
│   ├── __init__.py
│   ├── api.py                  # FastAPI application and endpoints
│   ├── config.py               # Configuration and API keys
│   ├── models.py               # Pydantic data models
│   ├── travel_planner_ui.py    # Streamlit user interface
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_service.py       # AI recommendation service
│   │   └── search_service.py   # Flight/hotel search service
│   └── utils/
│       ├── __init__.py
│       ├── formatters.py       # Data formatting utilities
│       └── transformers.py     # Data transformation utilities
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-planner.git
cd travel-planner
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install fastapi uvicorn streamlit pydantic crewai requests python-dotenv
```

### Environment Setup

1. Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SERP_API_KEY=your_serpapi_key_here
```

2. Get API Keys:
   - **Gemini API**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - **SerpAPI**: Get from [SerpAPI](https://serpapi.com/manage-api-key)

### Running the Application

#### Method 1: Run Both Services Separately

1. Start the FastAPI backend:
```bash
python main.py
```
The API will be available at `http://localhost:8000`

2. In a new terminal, start the Streamlit frontend:
```bash
streamlit run travel_planner/travel_planner_ui.py
```
The web interface will be available at `http://localhost:8501`

#### Method 2: API Only
```bash
python main.py
```
Then access the interactive API docs at `http://localhost:8000/docs`

## 📖 API Documentation

### Endpoints

#### `POST /search_flights/`
Search for flights between airports.

**Request Body:**
```json
{
  "origin": "HYD",
  "destination": "SYD", 
  "outbound_date": "2024-12-01",
  "return_date": "2024-12-10"
}
```

#### `POST /search_hotels/`
Search for hotels in a location.

**Request Body:**
```json
{
  "location": "SYD",
  "check_in_date": "2024-12-01",
  "check_out_date": "2024-12-10"
}
```

#### `POST /generate_itinerary/`
Generate a personalized travel itinerary.

**Request Body:**
```json
{
  "destination": "Sydney",
  "check_in_date": "2024-12-01", 
  "check_out_date": "2024-12-10",
  "flights": "Flight details...",
  "hotels": "Hotel details..."
}
```

## 🎯 Usage Examples

### Using the Web Interface

1. Navigate to `http://localhost:8501`
2. Enter your travel details (airports, dates, location)
3. Search for flights and hotels
4. View AI recommendations in the dedicated tab
5. Generate a personalized itinerary

### Using the API

```python
import requests

# Search flights
flight_data = {
    "origin": "HYD",
    "destination": "SYD",
    "outbound_date": "2024-12-01",
    "return_date": "2024-12-10"
}

response = requests.post("http://localhost:8000/search_flights/", json=flight_data)
result = response.json()
```

## 🔧 Configuration

Key configuration options in `config.py`:

- **GEMINI_API_KEY**: Your Google Gemini API key
- **SERP_API_KEY**: Your SerpAPI key for flight/hotel data
- **Logging**: Configured for INFO level with timestamps

## 🤖 AI Features

The application uses Google Gemini AI to provide:

- **Smart Flight Recommendations**: Analysis of price, duration, and convenience
- **Hotel Suggestions**: Ratings, location, and value analysis  
- **Itinerary Generation**: Day-by-day travel plans with activities and timing

## 🛠️ Development

### Project Dependencies

- **fastapi**: Web framework for the API
- **uvicorn**: ASGI server
- **streamlit**: Web UI framework
- **pydantic**: Data validation and settings management
- **crewai**: AI agent framework
- **requests**: HTTP library for API calls

### Adding New Features

1. Define new models in `models.py`
2. Add business logic to appropriate service files
3. Create API endpoints in `api.py`
4. Update the UI in `travel_planner_ui.py`

## 📊 Data Models

### FlightRequest
- `origin`: Departure airport code
- `destination`: Arrival airport code  
- `outbound_date`: Departure date (YYYY-MM-DD)
- `return_date`: Return date (YYYY-MM-DD)

### HotelRequest
- `location`: Hotel search location
- `check_in_date`: Check-in date (YYYY-MM-DD)
- `check_out_date`: Check-out date (YYYY-MM-DD)

### AIResponse
- `flights`: List of flight information
- `hotels`: List of hotel information
- `ai_flight_recommendation`: AI analysis of flights
- `ai_hotel_recommendation`: AI analysis of hotels
- `itinerary`: Generated travel itinerary

## 🚀 Deployment

### Local Development
Use the provided `main.py` with reload enabled for development.

### Production Deployment
For production, consider:
- Using environment variables for all sensitive configuration
- Setting up proper logging and monitoring
- Using a production ASGI server like Gunicorn
- Implementing rate limiting and authentication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Streamlit](https://streamlit.io/) for the rapid UI development
- [Google Gemini](https://ai.google.dev/) for AI capabilities
- [SerpAPI](https://serpapi.com/) for travel data

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:8000/docs) when running locally

---

**Happy Traveling!** ✈️🏨🗺️
