"""
Weather UI components for Mars Explorer Hub.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Optional

from src.utils.helpers import (
    celsius_to_fahrenheit,
    format_temperature,
    format_pressure,
    format_sol,
    get_temperature_color
)
import config


def render_weather_metrics(weather_df: Optional[pd.DataFrame], temp_unit: str = "C") -> None:
    """
    Render weather metrics in a column layout.
    
    Args:
        weather_df: DataFrame with weather data
        temp_unit: Temperature unit ('C' or 'F')
    """
    if weather_df is None or weather_df.empty:
        st.warning("⚠️ Weather data unavailable. InSight mission ended in December 2022.")
        st.info("ℹ️ Displaying historical Mars weather data from the InSight lander.")
        return
    
    # Get the latest sol data
    latest = weather_df.iloc[0]
    
    # Extract values
    sol = latest['sol']
    avg_temp_c = latest.get('avg_temp_c')
    min_temp_c = latest.get('min_temp_c')
    max_temp_c = latest.get('max_temp_c')
    pressure = latest.get('pressure_pa')
    season = latest.get('season', 'Unknown')
    
    # Convert temperatures if needed
    if temp_unit == "F":
        avg_temp = celsius_to_fahrenheit(avg_temp_c)
        min_temp = celsius_to_fahrenheit(min_temp_c)
        max_temp = celsius_to_fahrenheit(max_temp_c)
    else:
        avg_temp = avg_temp_c
        min_temp = min_temp_c
        max_temp = max_temp_c
    
    # Display metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🔴 Latest Sol",
            value=format_sol(sol),
            help="Martian day number since landing"
        )
    
    with col2:
        st.metric(
            label="🌡️ Avg Temperature",
            value=format_temperature(avg_temp, temp_unit),
            help=f"Average surface temperature on Sol {sol}"
        )
    
    with col3:
        st.metric(
            label="📊 Pressure",
            value=format_pressure(pressure),
            help="Atmospheric pressure in Pascals"
        )
    
    with col4:
        st.metric(
            label="🌅 Season",
            value=season,
            help="Current Martian season at InSight location"
        )
    
    # Display temperature range in an expander
    with st.expander("📈 Temperature Range Details"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"**Minimum:** {format_temperature(min_temp, temp_unit)}")
        with col_b:
            st.write(f"**Maximum:** {format_temperature(max_temp, temp_unit)}")


def render_temperature_chart(weather_df: Optional[pd.DataFrame], temp_unit: str = "C") -> None:
    """
    Render interactive temperature trends chart using Plotly.
    
    Args:
        weather_df: DataFrame with weather data
        temp_unit: Temperature unit ('C' or 'F')
    """
    if weather_df is None or weather_df.empty:
        return
    
    # Get last N sols for the chart
    chart_data = weather_df.head(config.MAX_SOLS_FOR_CHART).copy()
    chart_data = chart_data.sort_values('sol')  # Sort ascending for chart
    
    # Prepare temperature data
    if temp_unit == "F":
        chart_data['avg_temp'] = chart_data['avg_temp_c'].apply(celsius_to_fahrenheit)
        chart_data['min_temp'] = chart_data['min_temp_c'].apply(celsius_to_fahrenheit)
        chart_data['max_temp'] = chart_data['max_temp_c'].apply(celsius_to_fahrenheit)
        temp_label = "Temperature (°F)"
    else:
        chart_data['avg_temp'] = chart_data['avg_temp_c']
        chart_data['min_temp'] = chart_data['min_temp_c']
        chart_data['max_temp'] = chart_data['max_temp_c']
        temp_label = "Temperature (°C)"
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add temperature range as filled area
    fig.add_trace(go.Scatter(
        x=chart_data['sol'],
        y=chart_data['max_temp'],
        mode='lines',
        name='Max Temp',
        line=dict(color='rgba(255, 107, 53, 0.3)', width=0),
        showlegend=False,
        hovertemplate='Sol %{x}<br>Max: %{y:.1f}°<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=chart_data['sol'],
        y=chart_data['min_temp'],
        mode='lines',
        name='Temperature Range',
        line=dict(color='rgba(255, 107, 53, 0.3)', width=0),
        fillcolor='rgba(255, 107, 53, 0.2)',
        fill='tonexty',
        showlegend=True,
        hovertemplate='Sol %{x}<br>Min: %{y:.1f}°<extra></extra>'
    ))
    
    # Add average temperature line
    fig.add_trace(go.Scatter(
        x=chart_data['sol'],
        y=chart_data['avg_temp'],
        mode='lines+markers',
        name='Avg Temp',
        line=dict(color='#FF6B35', width=3),
        marker=dict(size=8, symbol='circle'),
        hovertemplate='Sol %{x}<br>Avg: %{y:.1f}°<extra></extra>'
    ))
    
    # Update layout with Mars theme
    fig.update_layout(
        title=f"Temperature Trends - Last {len(chart_data)} Sols",
        xaxis_title="Sol (Martian Day)",
        yaxis_title=temp_label,
        template="plotly_dark",
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(26, 31, 46, 0.8)',
        paper_bgcolor='rgba(11, 14, 26, 0.8)',
        font=dict(color='#E8E9ED'),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_unit_toggle() -> str:
    """
    Render temperature unit toggle and return selected unit.
    
    Returns:
        Selected temperature unit ('C' or 'F')
    """
    unit = st.radio(
        "🌡️ Temperature Unit:",
        options=["C", "F"],
        format_func=lambda x: "Celsius (°C)" if x == "C" else "Fahrenheit (°F)",
        horizontal=True,
        help="Toggle between Celsius and Fahrenheit"
    )
    return unit
