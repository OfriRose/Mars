#!/usr/bin/env python3
"""
Try different URL patterns based on MSL discovery to find Mars 2020 endpoint.
"""
import requests

# MSL pattern: /msl-raw-images/  
# Try variations for Mars 2020
patterns = [
    # Direct variations
    "https://mars.nasa.gov/m2020-raw-images/image/image_manifest.json",
    "https://mars.nasa.gov/mars2020-images/image/image_manifest.json",
    "https://mars.nasa.gov/perseverance-raw-images/image/image_manifest.json",
    
    # Under multimedia
    "https://mars.nasa.gov/mars2020/multimedia/raw/image_manifest.json",
    "https://mars.nasa.gov/mars2020/multimedia/images/image_manifest.json",
    
    # Try direct API calls like MSL
    "https://mars.nasa.gov/mars2020/images/image_manifest.json",
    
    # Check other mission patterns
    "https://mars.nasa.gov/mer-raw-images/image/image_manifest.json",  # MER (Opportunity/Spirit)
    "https://mars.nasa.gov/msl/multimedia/raw-images/image_manifest.json",
]

print("🔍 Searching for Mars 2020/Perseverance JSON manifest")
print("=" * 70)
print()

for url in patterns:
    identifier = url.split("/")[3] if len(url.split("/")) > 3 else "unknown"
    print(f"Testing [{identifier}]: {url}")
    
    try:
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        })
        
        if response.status_code == 200:
            print(f"✅ FOUND! Status: 200")
            try:
                data = response.json()
                print(f"   Type: {data.get('type', 'N/A')}")
                print(f"   Latest Sol: {data.get('latest_sol', 'N/A')}")
                print(f"   Total Images: {data.get('num_images', 'N/A'):,}")
                print(f"   Most Recent: {data.get('most_recent', 'N/A')}")
            except:
                print(f"   Content-Type: {response.headers.get('Content-Type')}")
                print(f"   Length: {len(response.text)} bytes")
        elif response.status_code == 403:
            print(f"⚠️  403 Forbidden")
        elif response.status_code == 404:
            print(f"❌ 404 Not Found")
        else:
            print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)[:50]}")
    print()
