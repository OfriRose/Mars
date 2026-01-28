"""
Photo gallery UI components for Mars Explorer Hub.
"""

import streamlit as st
from typing import List, Dict, Optional

from src.data.nasa_client import get_nasa_client


def render_photo_gallery(photos: Optional[List[Dict]]) -> None:
    """
    Render a gallery of Mars rover photos.
    
    Args:
        photos: List of photo dictionaries
    """
    if photos is None or len(photos) == 0:
        st.warning("⚠️ No photos available for this rover.")
        return
    
    st.subheader(f"📸 Latest {len(photos)} Photos from {photos[0]['rover']}")
    
    # Display photos in a grid
    cols = st.columns(min(len(photos), 3))
    
    for idx, photo in enumerate(photos):
        col_idx = idx % 3
        
        with cols[col_idx]:
            # Load and display image
            img = get_nasa_client().load_image_from_url(photo['img_src'])
            
            if img:
                st.image(img, use_container_width=True)
            else:
                st.error("Could not load image")
            
            # Display metadata in expander
            with st.expander(f"📋 Photo Details"):
                st.write(f"**Camera:** {photo['camera_name']}")
                st.write(f"**Sol:** {photo['sol']}")
                st.write(f"**Earth Date:** {photo['earth_date']}")
                st.write(f"**Photo ID:** {photo['id']}")


def render_rover_selector() -> str:
    """
    Render rover selection dropdown.
    
    Returns:
        Selected rover name (lowercase)
    """
    # Active rovers that regularly send photos
    active_rovers = ["curiosity", "perseverance"]
    
    rover = st.selectbox(
        "🤖 Select Mars Rover:",
        options=active_rovers,
        format_func=lambda x: x.capitalize(),
        help="Choose which rover's photos to display"
    )
    
    return rover
