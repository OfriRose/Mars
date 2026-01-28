"""
Configuration module for Mars Explorer Hub.
Handles API keys and application settings.
"""

import os
from typing import Optional

# Try to import streamlit for secrets management
try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def get_nasa_api_key() -> str:
    """
    Retrieve NASA API key from multiple sources in order of precedence:
    1. Streamlit secrets (for Streamlit Cloud deployment)
    2. Environment variables (for local development)
    3. Raise error if not found
    
    Returns:
        str: NASA API key
        
    Raises:
        ValueError: If API key is not found in any source
    """
    # Try Streamlit secrets first (for cloud deployment)
    if HAS_STREAMLIT and hasattr(st, 'secrets'):
        try:
            return st.secrets["NASA_API_KEY"]
        except (KeyError, FileNotFoundError):
            pass
    
    # Try environment variable
    api_key = os.getenv("NASA_API_KEY")
    if api_key:
        return api_key
    
    # If no key found, raise error with helpful message
    raise ValueError(
        "NASA API key not found. Please set it in one of:\n"
        "1. .streamlit/secrets.toml (for Streamlit Cloud)\n"
        "2. .env file (for local development)\n"
        "3. NASA_API_KEY environment variable"
    )


# NASA API Configuration
NASA_API_BASE_URL = "https://api.nasa.gov"
MARS_WEATHER_ENDPOINT = f"{NASA_API_BASE_URL}/insight_weather/"

# Mars Rover Images - New mars.nasa.gov JSON API (MSL/Curiosity only)
# Note: The old api.nasa.gov/mars-photos API was retired in late 2025
MSL_MANIFEST_URL = "https://mars.nasa.gov/msl-raw-images/image/image_manifest.json"
MSL_SOL_IMAGES_URL_TEMPLATE = "https://mars.nasa.gov/msl-raw-images/image/images_sol{sol}.json"

# Application Settings
CACHE_TTL_SECONDS = 3600  # 1 hour cache for API data
DEFAULT_NUM_PHOTOS = 5
MAX_SOLS_FOR_CHART = 7

# Rover Configuration
# Note: Only Curiosity is available due to API limitations
# Other rovers (Perseverance, Opportunity, Spirit) do not have accessible JSON APIs
AVAILABLE_ROVERS = ["curiosity"]
ROVER_DISPLAY_NAMES = {
    "curiosity": "Curiosity (MSL)"
}

# Camera mappings for rovers
ROVER_CAMERAS = {
    "curiosity": ["FHAZ", "RHAZ", "MAST", "CHEMCAM", "MAHLI", "MARDI", "NAVCAM"],
    "perseverance": ["EDL_RUCAM", "EDL_RDCAM", "EDL_DDCAM", "EDL_PUCAM1", 
                     "NAVCAM_LEFT", "NAVCAM_RIGHT", "MCZ_RIGHT", "MCZ_LEFT",
                     "FRONT_HAZCAM_LEFT_A", "FRONT_HAZCAM_RIGHT_A"],
    "opportunity": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"],
    "spirit": ["FHAZ", "RHAZ", "NAVCAM", "PANCAM", "MINITES"]
}
