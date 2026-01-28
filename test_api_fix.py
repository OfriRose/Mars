#!/usr/bin/env python3
"""
Quick test to verify the NASA API fix works.
"""
import requests

API_KEY = "Whrc0fN97eqwSdCGpdgA4O9PVhvVVbBh3H3aMJtW"
ROVER = "curiosity"

print(f"🔍 Testing NASA Mars Rover Photos API for {ROVER}...")
print()

# Test the new endpoint (latest_photos)
url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER}/latest_photos"
params = {"api_key": API_KEY}

print(f"📡 Requesting: {url}")
print(f"🔑 API Key: {API_KEY[:20]}...")
print()

try:
    response = requests.get(url, params=params, timeout=10)
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if 'latest_photos' in data:
            photos = data['latest_photos']
            print(f"✅ SUCCESS! Retrieved {len(photos)} photos")
            print()
            
            if photos:
                photo = photos[0]
                print("📸 Sample Photo Info:")
                print(f"   ID: {photo.get('id')}")
                print(f"   Sol: {photo.get('sol')}")
                print(f"   Earth Date: {photo.get('earth_date')}")
                print(f"   Camera: {photo.get('camera', {}).get('full_name')}")
                print(f"   Rover: {photo.get('rover', {}).get('name')}")
                print(f"   Image URL: {photo.get('img_src')[:60]}...")
        else:
            print("⚠️  Response structure unexpected")
            print(f"Keys in response: {list(data.keys())}")
    else:
        print(f"❌ HTTP Error {response.status_code}")
        print(f"Response: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Error: {e}")
