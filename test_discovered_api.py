#!/usr/bin/env python3
"""
Test the discovered mars.nasa.gov JSON endpoints for MSL (Curiosity) images.
"""
import requests
import json

print("🎉 Testing Discovered JSON API Endpoints")
print("=" * 70)
print()

# Test MSL manifest
print("1️⃣ Testing MSL Manifest...")
manifest_url = "https://mars.nasa.gov/msl-raw-images/image/image_manifest.json"

try:
    response = requests.get(manifest_url, timeout=10)
    if response.status_code == 200:
        manifest = response.json()
        print(f"✅ MSL Manifest loaded successfully!")
        print(f"Latest Sol: {manifest['latest_sol']}")
        print(f"Total Images: {manifest['num_images']:,}")
        print(f"Most Recent: {manifest['most_recent']}")
        print(f"Total Sols with data: {len(manifest['sols'])}")
        print()
        
        # Get the latest sol with images
        latest_sols = manifest['sols'][-5:]  # Last 5 sols
        print("Last 5 sols:")
        for sol_info in latest_sols:
            print(f"  Sol {sol_info['sol']}: {sol_info['num_images']} images - {sol_info['catalog_url']}")
        print()
        
        # Test loading images from a recent sol
        if latest_sols:
            test_sol = latest_sols[-1]
            print(f"2️⃣ Testing images from Sol {test_sol['sol']}...")
            print(f"URL: {test_sol['catalog_url']}")
            print()
            
            sol_response = requests.get(test_sol['catalog_url'], timeout=10)
            if sol_response.status_code == 200:
                sol_data = sol_response.json()
                print(f"✅ Sol {test_sol['sol']} catalog loaded!")
                print(f"Keys in response: {list(sol_data.keys())}")
                
                if 'images' in sol_data:
                    images = sol_data['images']
                    print(f"Number of images: {len(images)}")
                    print()
                    
                    # Show first image details
                    if images:
                        img = images[0]
                        print("Sample image data:")
                        for key, value in img.items():
                            if isinstance(value, str) and len(str(value)) > 100:
                                print(f"  {key}: {str(value)[:100]}...")
                            else:
                                print(f"  {key}: {value}")
            else:
                print(f"❌ Failed to load sol catalog: {sol_response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print()
print("=" * 70)
print("3️⃣ Checking for Mars 2020 (Perseverance) equivalent...")

# Try similar pattern for Mars 2020
mars2020_patterns = [
    "https://mars.nasa.gov/mars2020/multimedia/raw-images/image_manifest.json",
    "https://mars.nasa.gov/mars2020-raw-images/image/image_manifest.json",
    "https://mars.nasa.gov/mars2020/multimedia/raw-images/manifest.json",
]

for url in mars2020_patterns:
    print(f"Testing: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Status: 200 - FOUND!")
            try:
                data = response.json()
                print(f"Keys: {list(data.keys())}")
            except:
                print(f"Not JSON, content-type: {response.headers.get('Content-Type')}")
        else:
            print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {type(e).__name__}")
    print()
