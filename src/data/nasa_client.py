"""
NASA API client for Mars Explorer Hub.
Handles all interactions with NASA's Mars data APIs.
"""

import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from io import BytesIO
from PIL import Image

import config


class NASAClient:
    """Client for interacting with NASA Mars APIs."""
    
    def __init__(self):
        """Initialize the NASA API client with API key."""
        self.api_key = config.get_nasa_api_key()
        self.session = requests.Session()
        self.session.params = {'api_key': self.api_key}
    
    def _make_request(self, url: str, params: Optional[Dict] = None, timeout: int = 10) -> Optional[Dict]:
        """
        Make HTTP request with error handling and retries.
        
        Args:
            url: API endpoint URL
            params: Optional query parameters
            timeout: Request timeout in seconds
            
        Returns:
            JSON response as dictionary or None if request failed
        """
        try:
            response = self.session.get(url, params=params, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timeout - NASA servers might be slow. Please try again.")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                st.error("🚫 Rate limit exceeded. Please wait a moment before refreshing.")
            else:
                st.error(f"❌ HTTP Error {e.response.status_code}: {str(e)}")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"🌐 Network error: {str(e)}")
            return None
    
    @st.cache_data(ttl=config.CACHE_TTL_SECONDS, show_spinner=False)
    def get_mars_weather(_self) -> Optional[pd.DataFrame]:
        """
        Fetch Mars weather data from NASA InSight API.
        
        Note: InSight mission ended in December 2022, so this returns historical data.
        
        Returns:
            DataFrame with columns: sol, min_temp, max_temp, pressure, season
            Returns None if data unavailable
        """
        url = config.MARS_WEATHER_ENDPOINT
        params = {"feedtype": "json", "ver": "1.0"}
        
        data = _self._make_request(url, params)
        
        if not data:
            return None
        
        # InSight API returns data in a nested structure
        # Extract Sol data (skip metadata keys)
        sol_keys = [key for key in data.keys() if key.isdigit()]
        
        if not sol_keys:
            st.warning("⚠️ No weather data available. InSight mission ended in December 2022.")
            return None
        
        # Parse weather data into structured format
        weather_records = []
        for sol in sol_keys:
            sol_data = data[sol]
            
            # Extract temperature data (if available)
            temp_data = sol_data.get('AT', {})
            min_temp = temp_data.get('mn')
            max_temp = temp_data.get('mx')
            avg_temp = temp_data.get('av')
            
            # Extract pressure data (if available)
            pressure_data = sol_data.get('PRE', {})
            avg_pressure = pressure_data.get('av')
            
            # Get season
            season = sol_data.get('Season', 'Unknown')
            
            # Get Earth date
            first_utc = sol_data.get('First_UTC')
            
            weather_records.append({
                'sol': int(sol),
                'min_temp_c': min_temp,
                'max_temp_c': max_temp,
                'avg_temp_c': avg_temp,
                'pressure_pa': avg_pressure,
                'season': season,
                'earth_date': first_utc
            })
        
        # Convert to DataFrame and sort by Sol
        df = pd.DataFrame(weather_records)
        df = df.sort_values('sol', ascending=False)
        
        return df
    
    @st.cache_data(ttl=config.CACHE_TTL_SECONDS, show_spinner=False)
    def get_rover_photos(_self, rover_name: str, num_photos: int = 5) -> Optional[List[Dict]]:
        """
        Fetch latest photos from a Mars rover.
        
        Note: Currently only supports Curiosity (MSL) rover using mars.nasa.gov JSON API.
        The old api.nasa.gov Mars Rover Photos API was retired in late 2025.
        
        Args:
            rover_name: Name of rover (currently only 'curiosity' is supported)
            num_photos: Number of photos to retrieve
            
        Returns:
            List of photo dictionaries with keys: img_src, camera, sol, earth_date
            Returns None if no photos available
        """
        rover_name = rover_name.lower()
        
        # Only Curiosity is supported with the current API
        if rover_name != "curiosity":
            st.warning(f"⚠️ {rover_name.title()} rover is not currently available. Only Curiosity rover is supported.")
            return None
        
        # Fetch MSL manifest to get latest sol
        manifest_data = _self._make_request(config.MSL_MANIFEST_URL)
        
        if not manifest_data:
            st.error("❌ Could not retrieve Curiosity rover manifest")
            return None
        
        # Get the latest sol with images
        sols = manifest_data.get('sols', [])
        if not sols:
            st.warning("⚠️ No image data available in manifest")
            return None
        
        # Find the most recent sol with images (iterate backwards)
        latest_sol = None
        for sol_info in reversed(sols):
            if sol_info.get('num_images', 0) > 0:
                latest_sol = sol_info['sol']
                break
        
        if latest_sol is None:
            st.warning("⚠️ No recent photos found for Curiosity")
            return None
        
        # Fetch images for the latest sol
        sol_images_url = config.MSL_SOL_IMAGES_URL_TEMPLATE.format(sol=latest_sol)
        sol_data = _self._make_request(sol_images_url)
        
        if not sol_data or 'images' not in sol_data:
            st.error(f"❌ Could not retrieve images for Sol {latest_sol}")
            return None
        
        images = sol_data['images'][:num_photos]
        
        if not images:
            st.warning(f"⚠️ No images found for Sol {latest_sol}")
            return None
        
        # Format photo data to match expected structure
        formatted_photos = []
        for img in images:
            # Extract URL - the urlList field contains the full image URL
            img_url = img.get('urlList', '')
            
            # Parse UTC timestamp to extract date
            utc_timestamp = img.get('utc', '')
            earth_date = utc_timestamp.split('T')[0] if 'T' in utc_timestamp else utc_timestamp
            
            # Map instrument name to camera name
            instrument = img.get('instrument', 'Unknown')
            camera_name = _self._format_camera_name(instrument)
            
            formatted_photos.append({
                'id': img.get('itemName', 'unknown'),
                'img_src': img_url,
                'camera_name': camera_name,
                'camera_abbr': instrument,
                'sol': int(img.get('sol', latest_sol)),
                'earth_date': earth_date,
                'rover': 'Curiosity'
            })
        
        return formatted_photos
    
    def _format_camera_name(self, instrument: str) -> str:
        """
        Convert MSL instrument codes to readable camera names.
        
        Args:
            instrument: Instrument code (e.g., 'NAV_RIGHT_B', 'MAST_LEFT')
            
        Returns:
            Human-readable camera name
        """
        # Common MSL camera mappings
        camera_map = {
            'NAV_LEFT': 'Navigation Camera - Left',
            'NAV_RIGHT': 'Navigation Camera - Right',
            'NAV_LEFT_B': 'Navigation Camera - Left B',
            'NAV_RIGHT_B': 'Navigation Camera - Right B',
            'FHAZ_LEFT': 'Front Hazard Avoidance Camera - Left',
            'FHAZ_RIGHT': 'Front Hazard Avoidance Camera - Right',
            'RHAZ_LEFT': 'Rear Hazard Avoidance Camera - Left',
            'RHAZ_RIGHT': 'Rear Hazard Avoidance Camera - Right',
            'MAST_LEFT': 'Mast Camera - Left',
            'MAST_RIGHT': 'Mast Camera - Right',
            'MAHLI': 'Mars Hand Lens Imager',
            'MARDI': 'Mars Descent Imager',
            'CHEMCAM': 'Chemistry and Camera Complex'
        }
        
        # Try exact match first
        if instrument in camera_map:
            return camera_map[instrument]
        
        # Try partial matches (e.g., 'NAV_RIGHT_B' -> 'Navigation Camera')
        for key, value in camera_map.items():
            if instrument.startswith(key):
                return value
        
        # Default: return cleaned up instrument name
        return instrument.replace('_', ' ').title()
    
    @st.cache_data(ttl=config.CACHE_TTL_SECONDS, show_spinner=False)
    def load_image_from_url(_self, url: str) -> Optional[Image.Image]:
        """
        Load an image from a URL.
        
        Args:
            url: Image URL
            
        Returns:
            PIL Image object or None if loading failed
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content))
            return img
        except Exception as e:
            st.warning(f"⚠️ Could not load image: {str(e)}")
            return None


# Create a singleton instance
nasa_client = NASAClient()
