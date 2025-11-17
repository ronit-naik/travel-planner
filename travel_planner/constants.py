"""
Constants and configuration mappings for the travel planner application.
"""

# Airport code to city name mapping for better search results
AIRPORT_TO_CITY = {
    # Australia & Oceania
    "SYD": "Sydney, Australia",
    "MEL": "Melbourne, Australia", 
    "BNE": "Brisbane, Australia",
    "PER": "Perth, Australia",
    "ADL": "Adelaide, Australia",
    "DRW": "Darwin, Australia",
    "CNS": "Cairns, Australia",
    "GLD": "Gold Coast, Australia",
    "AKL": "Auckland, New Zealand",
    "CHC": "Christchurch, New Zealand",
    
    # North America - USA
    "NYC": "New York City, USA",
    "JFK": "New York City, USA",
    "LGA": "New York City, USA",
    "EWR": "New York City, USA",
    "LAX": "Los Angeles, USA",
    "SFO": "San Francisco, USA",
    "CHI": "Chicago, USA",
    "ORD": "Chicago, USA",
    "MDW": "Chicago, USA",
    "MIA": "Miami, USA",
    "LAS": "Las Vegas, USA",
    "SEA": "Seattle, USA",
    "DEN": "Denver, USA",
    "ATL": "Atlanta, USA",
    "BOS": "Boston, USA",
    "DFW": "Dallas, USA",
    "IAH": "Houston, USA",
    "PHX": "Phoenix, USA",
    "MSP": "Minneapolis, USA",
    "DTW": "Detroit, USA",
    
    # North America - Canada
    "YYZ": "Toronto, Canada",
    "YVR": "Vancouver, Canada",
    "YUL": "Montreal, Canada",
    "YYC": "Calgary, Canada",
    "YOW": "Ottawa, Canada",
    "YWG": "Winnipeg, Canada",
    
    # Europe - UK & Ireland
    "LHR": "London, UK",
    "LGW": "London, UK", 
    "STN": "London, UK",
    "LTN": "London, UK",
    "MAN": "Manchester, UK",
    "EDI": "Edinburgh, UK",
    "GLA": "Glasgow, UK",
    "DUB": "Dublin, Ireland",
    
    # Europe - Continental
    "CDG": "Paris, France",
    "ORY": "Paris, France",
    "FRA": "Frankfurt, Germany",
    "MUC": "Munich, Germany",
    "DUS": "Dusseldorf, Germany",
    "BER": "Berlin, Germany",
    "BCN": "Barcelona, Spain",
    "MAD": "Madrid, Spain",
    "FCO": "Rome, Italy",
    "MXP": "Milan, Italy",
    "VCE": "Venice, Italy",
    "AMS": "Amsterdam, Netherlands",
    "ZUR": "Zurich, Switzerland",
    "VIE": "Vienna, Austria",
    "CPH": "Copenhagen, Denmark",
    "ARN": "Stockholm, Sweden",
    "OSL": "Oslo, Norway",
    "HEL": "Helsinki, Finland",
    
    # Asia - East Asia
    "NRT": "Tokyo, Japan",
    "HND": "Tokyo, Japan",
    "KIX": "Osaka, Japan",
    "ICN": "Seoul, South Korea",
    "PVG": "Shanghai, China",
    "PEK": "Beijing, China",
    "CAN": "Guangzhou, China",
    "HKG": "Hong Kong",
    "TPE": "Taipei, Taiwan",
    
    # Asia - Southeast Asia
    "SIN": "Singapore",
    "BKK": "Bangkok, Thailand",
    "KUL": "Kuala Lumpur, Malaysia",
    "CGK": "Jakarta, Indonesia",
    "MNL": "Manila, Philippines",
    "SGN": "Ho Chi Minh City, Vietnam",
    "HAN": "Hanoi, Vietnam",
    
    # Asia - South Asia & Middle East
    "BOM": "Mumbai, India",
    "DEL": "New Delhi, India",
    "BLR": "Bangalore, India",
    "MAA": "Chennai, India",
    "CCU": "Kolkata, India",
    "DXB": "Dubai, UAE",
    "AUH": "Abu Dhabi, UAE",
    "DOH": "Doha, Qatar",
    "RUH": "Riyadh, Saudi Arabia",
    "JED": "Jeddah, Saudi Arabia",
    
    # Africa
    "CAI": "Cairo, Egypt",
    "JNB": "Johannesburg, South Africa",
    "CPT": "Cape Town, South Africa",
    "LOS": "Lagos, Nigeria",
    "ADD": "Addis Ababa, Ethiopia",
    
    # South America
    "GRU": "São Paulo, Brazil",
    "GIG": "Rio de Janeiro, Brazil",
    "EZE": "Buenos Aires, Argentina",
    "SCL": "Santiago, Chile",
    "LIM": "Lima, Peru",
    "BOG": "Bogotá, Colombia",
}

# Airport code to country code mapping for geographic search bias
AIRPORT_TO_COUNTRY = {
    # Australia & Oceania
    "SYD": "au", "MEL": "au", "BNE": "au", "PER": "au", "ADL": "au", 
    "DRW": "au", "CNS": "au", "GLD": "au",
    "AKL": "nz", "CHC": "nz",
    
    # North America - USA
    "NYC": "us", "JFK": "us", "LGA": "us", "EWR": "us", "LAX": "us", 
    "SFO": "us", "CHI": "us", "ORD": "us", "MDW": "us", "MIA": "us", 
    "LAS": "us", "SEA": "us", "DEN": "us", "ATL": "us", "BOS": "us", 
    "DFW": "us", "IAH": "us", "PHX": "us", "MSP": "us", "DTW": "us",
    
    # North America - Canada
    "YYZ": "ca", "YVR": "ca", "YUL": "ca", "YYC": "ca", "YOW": "ca", "YWG": "ca",
    
    # Europe - UK & Ireland
    "LHR": "uk", "LGW": "uk", "STN": "uk", "LTN": "uk", "MAN": "uk", 
    "EDI": "uk", "GLA": "uk", "DUB": "ie",
    
    # Europe - Continental
    "CDG": "fr", "ORY": "fr", 
    "FRA": "de", "MUC": "de", "DUS": "de", "BER": "de",
    "BCN": "es", "MAD": "es", 
    "FCO": "it", "MXP": "it", "VCE": "it",
    "AMS": "nl", "ZUR": "ch", "VIE": "at", "CPH": "dk", 
    "ARN": "se", "OSL": "no", "HEL": "fi",
    
    # Asia - East Asia
    "NRT": "jp", "HND": "jp", "KIX": "jp",
    "ICN": "kr", 
    "PVG": "cn", "PEK": "cn", "CAN": "cn",
    "HKG": "hk", "TPE": "tw",
    
    # Asia - Southeast Asia
    "SIN": "sg", "BKK": "th", "KUL": "my", "CGK": "id", 
    "MNL": "ph", "SGN": "vn", "HAN": "vn",
    
    # Asia - South Asia & Middle East
    "BOM": "in", "DEL": "in", "BLR": "in", "MAA": "in", "CCU": "in",
    "DXB": "ae", "AUH": "ae", "DOH": "qa", "RUH": "sa", "JED": "sa",
    
    # Africa
    "CAI": "eg", "JNB": "za", "CPT": "za", "LOS": "ng", "ADD": "et",
    
    # South America
    "GRU": "br", "GIG": "br", "EZE": "ar", "SCL": "cl", 
    "LIM": "pe", "BOG": "co",
}

# Default search parameters
DEFAULT_FLIGHT_PARAMS = {
    "hl": "en",
    "currency": "USD"
}

DEFAULT_HOTEL_PARAMS = {
    "hl": "en",
    "currency": "USD",
    "sort_by": 3,  # Sort by rating
    "rating": 8    # Minimum rating filter
}

# Search engine configurations
SEARCH_ENGINES = {
    "flights": "google_flights",
    "hotels": "google_hotels"
}

# Default country code for unknown locations
DEFAULT_COUNTRY_CODE = "us"
