"""
Mars Explorer Hub - Main Streamlit Application
A dashboard for real-time Martian weather and rover imagery from NASA.
"""

import streamlit as st

from src.data.nasa_client import get_nasa_client
from src.ui import (
    render_weather_metrics,
    render_temperature_chart,
    render_unit_toggle,
    render_photo_gallery,
    render_rover_selector
)
import config


# Page configuration
st.set_page_config(
    page_title="Mars Explorer Hub",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    h1 {
        color: #FF6B35;
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #B8B8B8;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 107, 53, 0.3);
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.title("🔴 Mars Explorer Hub")
    st.markdown('<p class="subtitle">Real-time Martian Weather & Rover Imagery from NASA</p>', 
                unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Temperature unit toggle
        temp_unit = render_unit_toggle()
        
        st.divider()
        
        # Rover selection
        st.header("🤖 Rover Selection")
        selected_rover = render_rover_selector()
        
        st.divider()
        
        # Info section
        st.header("ℹ️ About")
        st.info(
            "**Mars Explorer Hub** displays real-time data from NASA's Mars missions:\n\n"
            "- 🌡️ **Weather Data**: Historical atmospheric conditions from InSight lander\n"
            "- 📸 **Rover Photos**: Latest images from active Mars rovers\n\n"
            "Data refreshes automatically every hour."
        )
        
        # Credits
        st.caption("Data provided by NASA's Open APIs")
        st.caption("[api.nasa.gov](https://api.nasa.gov)")
    
    # Main content area
    try:
        # Weather Section
        st.header("🌡️ Martian Weather Conditions")
        
        with st.spinner("Fetching Mars weather data..."):
            weather_df = get_nasa_client().get_mars_weather()
        
        # Display weather metrics
        render_weather_metrics(weather_df, temp_unit)
        
        st.divider()
        
        # Temperature trends chart
        if weather_df is not None and not weather_df.empty:
            st.subheader("📊 Temperature Trends")
            render_temperature_chart(weather_df, temp_unit)
        
        st.divider()
        
        # Rover Photos Section
        st.header(f"📸 {selected_rover.capitalize()} Rover Photos")
        
        with st.spinner(f"Loading latest photos from {selected_rover.capitalize()}..."):
            photos = get_nasa_client().get_rover_photos(
                rover_name=selected_rover,
                num_photos=config.DEFAULT_NUM_PHOTOS
            )
        
        render_photo_gallery(photos)
        
    except ValueError as e:
        # Handle API key errors
        st.error("🔑 API Configuration Error")
        st.error(str(e))
        st.info(
            "**For local development:**\n"
            "1. Create a `.streamlit/secrets.toml` file\n"
            "2. Add your NASA API key: `NASA_API_KEY = \"your_key\"`\n\n"
            "**For Streamlit Cloud:**\n"
            "1. Go to App Settings → Secrets\n"
            "2. Add: `NASA_API_KEY = \"your_key\"`"
        )
    
    except Exception as e:
        # Handle unexpected errors
        st.error("❌ An unexpected error occurred")
        st.error(str(e))
        st.info("Please try refreshing the page or check your internet connection.")
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #888; padding: 2rem 0;'>
            Made with ❤️ using Streamlit | Data from NASA Mars Rover APIs<br>
            <small>InSight weather data is historical (mission ended Dec 2022)</small>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
