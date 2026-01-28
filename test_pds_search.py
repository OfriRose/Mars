#!/usr/bin/env python3
"""
Test PDS Search API (newer API for PDS4 data).
"""
import requests
import json

# Try multiple PDS endpoints
endpoints = [
    {
        "name": "PDS Search API v1.3",
        "url": "https://pds.nasa.gov/api/search/1.3/products",
        "params": {
            "q": "(lid:*mars*curiosity* OR lid:*msl*) AND pds:Product_Observational",
            "limit": 5
        }
    },
    {
        "name": "PDS Search API v1 (older)",
        "url": "https://pds.nasa.gov/api/search/1/products",
        "params": {
            "q": "mars curiosity",
            "limit": 5
        }
    },
    {
        "name": "PDS Registry API",
        "url": "https://pds.nasa.gov/api/registry/0.1/products",
        "params": {
            "q": "mars",
            "limit": 5
        }
    }
]

print("🔍 Testing PDS Search APIs")
print("=" * 70)
print()

for endpoint in endpoints:
    print(f"📡 API: {endpoint['name']}")
    print(f"URL: {endpoint['url']}")
    print(f"Params: {endpoint['params']}")
    print()
    
    try:
        response = requests.get(endpoint['url'], params=endpoint.get('params'), timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ SUCCESS!")
                print(f"Response keys: {list(data.keys())}")
                print(json.dumps(data, indent=2)[:800])
            except json.JSONDecodeError:
                print(f"Response (text): {response.text[:500]}")
        else:
            print(f"❌ HTTP Error {response.status_code}")
            print(f"Response: {response.text[:300]}")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
    
    print()
    print("-" * 70)
    print()

# Also test if there are public rover image endpoints
print("🔍 Testing alternative Mars rover data sources")
print("=" * 70)
print()

# Try Mars Science Laboratory Raw Images (PDS Geosciences Node)
msl_url = "https://pds-geosciences.wustl.edu/msl/msl-m-mastcam-4-rdr-image-v1/mslmst_0001/"
print(f"Testing MSL Data Access: {msl_url}")
try:
    response = requests.head(msl_url, timeout=10)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ MSL data directory is accessible!")
except Exception as e:
    print(f"❌ Error: {e}")
