#!/usr/bin/env python3
"""
Test direct PDS data access through file servers and ODE (Orbital Data Explorer).
"""
import requests

endpoints = [
    {
        "name": "PDS Geosciences - MSL (Curiosity) Browse",
        "url": "https://pds-geosciences.wustl.edu/missions/msl/"
    },
    {
        "name": "PDS Geosciences - Mars 2020 (Perseverance) Browse",  
        "url": "https://pds-geosciences.wustl.edu/missions/mars2020/"
    },
    {
        "name": "ODE REST API - Mars Images",
        "url": "https://oderest.rsl.wustl.edu/livemars2/api/missions"
    },
    {
        "name": "PDS Image Atlas (alternate URL)",
        "url": "https://pds-imaging.jpl.nasa.gov/portal/mars_mission.html"
    },
    {
        "name": "Mars Raw Images Portal (JPL)",
        "url": "https://mars.nasa.gov/mars2020/multimedia/raw-images/"
    }
]

print("🔍 Testing Direct PDS Data Access")
print("=" * 70)
print()

for endpoint in endpoints:
    print(f"Testing: {endpoint['name']}")
    print(f"URL: {endpoint['url']}")
    
    try:
        response = requests.head(endpoint['url'], timeout=10, allow_redirects=True)
        status = response.status_code
        
        if status == 200:
            print(f"✅ Status: {status} - ACCESSIBLE!")
        else:
            print(f"⚠️  Status: {status}")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
    
    print()

# Test ODE REST API specifically
print("=" * 70)
print("🔍 Testing ODE (Orbital Data Explorer) REST API")
print()

ode_base = "https://oderest.rsl.wustl.edu/live2/odelte"
test_query = {
    "query": "mars",
    "output": "json",
    "limit": 5,
    "product": "MSLmast"  # MSL Mastcam images
}

try:
    response = requests.get(ode_base, params=test_query, timeout=15)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ ODE API is accessible!")
        print(f"Response length: {len(response.text)} bytes")
        print(f"First 500 chars:\n{response.text[:500]}")
    else:
        print(f"Response: {response.text[:300]}")
except Exception as e:
    print(f"❌ Error: {e}")
