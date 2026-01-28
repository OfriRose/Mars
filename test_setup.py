"""
Quick test script to verify the Mars Explorer Hub setup.
"""

import sys

print("🔍 Testing Mars Explorer Hub Components...")
print()

# Test 1: Import configuration
print("1️⃣ Testing configuration module...")
try:
    import config
    print("   ✅ Config module imported successfully")
    print(f"   📡 NASA API Base URL: {config.NASA_API_BASE_URL}")
    print(f"   ⏱️  Cache TTL: {config.CACHE_TTL_SECONDS}s")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 2: Test API key configuration
print()
print("2️⃣ Testing API key configuration...")
try:
    api_key = config.get_nasa_api_key()
    print(f"   ✅ API key loaded successfully (length: {len(api_key)})")
    print(f"   🔑 API key preview: {api_key[:10]}...")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 3: Import NASA client
print()
print("3️⃣ Testing NASA client module...")
try:
    from src.data.nasa_client import nasa_client
    print("   ✅ NASA client imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 4: Import utility functions
print()
print("4️⃣ Testing utility functions...")
try:
    from src.utils import celsius_to_fahrenheit, format_temperature
    temp_c = -63.5
    temp_f = celsius_to_fahrenheit(temp_c)
    print(f"   ✅ Utils imported successfully")
    print(f"   🌡️  Test conversion: {temp_c}°C = {temp_f:.1f}°F")
    print(f"   📝 Formatted: {format_temperature(temp_c, 'C')}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 5: Import UI components
print()
print("5️⃣ Testing UI components...")
try:
    from src.ui import (
        render_weather_metrics,
        render_temperature_chart,
        render_photo_gallery,
        render_rover_selector
    )
    print("   ✅ All UI components imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Test 6: Import main app
print()
print("6️⃣ Testing main app module...")
try:
    import app
    print("   ✅ Main app module imported successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

print()
print("=" * 60)
print("🎉 All tests passed! Mars Explorer Hub is ready to launch!")
print("=" * 60)
print()
print("To run the app:")
print("  ./venv/bin/streamlit run app.py")
print()
