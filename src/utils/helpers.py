"""
Utility functions for Mars Explorer Hub.
"""

from typing import Optional


def celsius_to_fahrenheit(celsius: Optional[float]) -> Optional[float]:
    """
    Convert temperature from Celsius to Fahrenheit.
    
    Args:
        celsius: Temperature in Celsius
        
    Returns:
        Temperature in Fahrenheit or None if input is None
    """
    if celsius is None:
        return None
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: Optional[float]) -> Optional[float]:
    """
    Convert temperature from Fahrenheit to Celsius.
    
    Args:
        fahrenheit: Temperature in Fahrenheit
        
    Returns:
        Temperature in Celsius or None if input is None
    """
    if fahrenheit is None:
        return None
    return (fahrenheit - 32) * 5/9


def format_temperature(temp: Optional[float], unit: str = "C") -> str:
    """
    Format temperature value for display.
    
    Args:
        temp: Temperature value
        unit: Temperature unit ('C' or 'F')
        
    Returns:
        Formatted temperature string
    """
    if temp is None:
        return "N/A"
    
    symbol = "°C" if unit == "C" else "°F"
    return f"{temp:.1f}{symbol}"


def format_pressure(pressure: Optional[float]) -> str:
    """
    Format pressure value for display.
    
    Args:
        pressure: Pressure in Pascals
        
    Returns:
        Formatted pressure string
    """
    if pressure is None:
        return "N/A"
    
    return f"{pressure:.0f} Pa"


def format_sol(sol: int) -> str:
    """
    Format Martian Sol number for display.
    
    Args:
        sol: Sol number
        
    Returns:
        Formatted sol string
    """
    return f"Sol {sol}"


def get_temperature_color(temp_c: Optional[float]) -> str:
    """
    Get a color code based on temperature.
    Useful for styling temperature displays.
    
    Args:
        temp_c: Temperature in Celsius
        
    Returns:
        CSS color code
    """
    if temp_c is None:
        return "#888888"  # Gray for N/A
    
    # Mars temperatures typically range from -125°C to 20°C
    if temp_c > 0:
        return "#FF6B35"  # Warm orange
    elif temp_c > -40:
        return "#4ECDC4"  # Teal
    elif temp_c > -80:
        return "#4A90E2"  # Blue
    else:
        return "#B8E6F0"  # Light blue for very cold
