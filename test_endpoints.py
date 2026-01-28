#!/usr/bin/env python3
"""
Test multiple NASA API endpoints to find what works.
"""
import requests

API_KEY = "Whrc0fN97eqwSdCGpdgA4O9PVhvVVbBh3H3aMJtW"
ROVER = "curiosity"

endpoints = [
    ("Latest Photos", f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER}/latest_photos"),
    ("Manifest", f"https://api.nasa.gov/mars-photos/api/v1/manifests/{ROVER}"),
    ("Photos by Sol 1000", f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER}/photos?sol=1000"),
    ("Photos by Earth Date", f"https://api.nasa.gov/mars-photos/api/v1/rovers/{ROVER}/photos?earth_date=2015-06-03"),
]

print("🔍 Testing NASA Mars Rover Photos API endpoints...")
print()

for name, url in endpoints:
    print(f"Testing: {name}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url, params={"api_key": API_KEY}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # Print first level keys
            print(f"✅ SUCCESS! Keys: {list(data.keys())}")
            
            # Show count if available
            if 'photos' in data:
                print(f"   Photos count: {len(data['photos'])}")
            if 'latest_photos' in data:
                print(f"   Latest photos count: {len(data['latest_photos'])}")
        else:
            print(f"❌ Failed - Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("-" * 60)
    print()
