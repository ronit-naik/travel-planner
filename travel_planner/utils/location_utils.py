"""
Location utility functions for handling airport codes and city conversions.
"""

from typing import Optional
from ..constants import AIRPORT_TO_CITY, AIRPORT_TO_COUNTRY, DEFAULT_COUNTRY_CODE


def convert_airport_code_to_city(location: str) -> str:
    """
    Convert airport code to full city name for better hotel search.
    
    Args:
        location: Airport code (e.g., 'SYD', 'LAX') or city name
        
    Returns:
        Full city name with country (e.g., 'Sydney, Australia')
    """
    if not location:
        return location
        
    location_upper = location.strip().upper()
    return AIRPORT_TO_CITY.get(location_upper, location)


def get_country_code_for_location(location: str) -> str:
    """
    Get appropriate country code for geographic search bias.
    
    Args:
        location: Airport code or city name
        
    Returns:
        Two-letter country code (e.g., 'au', 'us', 'uk')
    """
    if not location:
        return DEFAULT_COUNTRY_CODE
        
    location_upper = location.strip().upper()
    return AIRPORT_TO_COUNTRY.get(location_upper, DEFAULT_COUNTRY_CODE)


def is_airport_code(location: str) -> bool:
    """
    Check if the given location string is a recognized airport code.
    
    Args:
        location: Location string to check
        
    Returns:
        True if location is a known airport code, False otherwise
    """
    if not location:
        return False
        
    location_upper = location.strip().upper()
    return location_upper in AIRPORT_TO_CITY


def get_location_info(location: str) -> dict:
    """
    Get comprehensive location information including city name and country code.
    
    Args:
        location: Airport code or city name
        
    Returns:
        Dictionary containing 'city_name', 'country_code', and 'is_airport_code'
    """
    return {
        'city_name': convert_airport_code_to_city(location),
        'country_code': get_country_code_for_location(location),
        'is_airport_code': is_airport_code(location),
        'original': location
    }
