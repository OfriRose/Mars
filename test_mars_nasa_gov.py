#!/usr/bin/env python3
"""
Try to find mars.nasa.gov JSON API endpoints by testing common patterns.
"""
import requests
import json

# Common API endpoint patterns for mars.nasa.gov
test_endpoints = [
    # Try API subdomain
    "https://api.mars.nasa.gov/mars2020/photos",
    "https://api.mars.nasa.gov/mars2020/latest",
    
    # Try JSON endpoints under main domain
    "https://mars.nasa.gov/api/v1/mars2020/photos",
    "https://mars.nasa.gov/rss/api/?feed=raw_images&category=mars2020",
    "https://mars.nasa.gov/msl-raw-images/image/image_manifest.json",
    
    # Try data subdomain
    "https://data.mars.nasa.gov/mars2020/photos",
    
    # Try direct feed URLs
    "https://mars.nasa.gov/rss/api/?feed=raw_images_mars2020",
    "https://mars.nasa.gov/feeds/raw_images/?feedtype=json",
]

print("🔍 Searching for mars.nasa.gov JSON API Endpoints")
print("=" * 70)
print()

for url in test_endpoints:
    print(f"Testing: {url}")
    
    try:
        # Try both GET with common params
        response = requests.get(url, timeout=10, headers={
            'User-Agent': 'Mozilla/5.0 (Python Requests)',
            'Accept': 'application/json'
        })
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            print(f"Content-Type: {content_type}")
            
            if 'json' in content_type.lower() or url.endswith('.json'):
                print("✅ JSON ENDPOINT FOUND!")
                try:
                    data = response.json()
                    print(f"Response keys: {list(data.keys())}")
                    print(f"Sample: {json.dumps(data, indent=2)[:500]}")
                except:
                    print(f"Response text: {response.text[:500]}")
            else:
                print(f"Response preview: {response.text[:200]}")
        elif response.status_code == 404:
            print("❌ Not Found")
        elif response.status_code in [301, 302, 307, 308]:
            print(f"🔀 Redirect to: {response.headers.get('Location')}")
        else:
            print(f"⚠️  Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}")
    
    print()

print("=" * 70)
print("🔍 Checking for RSS/XML feeds (can be converted to JSON)")
print()

rss_feeds = [
    "https://mars.nasa.gov/rss/api/?feed=raw_images&category=mars2020,msl",
    "https://mars.nasa.gov/msl/multimedia/raw-images/rss.xml",
    "https://mars.nasa.gov/mars2020/multimedia/raw-images/rss.xml",
]

for url in rss_feeds:
    print(f"Testing: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Status: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type')}")
            print(f"Length: {len(response.text)} bytes")
        else:
            print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    print()
