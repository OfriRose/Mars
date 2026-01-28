#!/usr/bin/env python3
"""
Test PDS Imaging Atlas Search API to find Mars rover images.
"""
import requests
import json

# PDS Imaging Atlas Search API endpoint
BASE_URL = "https://pds-imaging.jpl.nasa.gov/solr/pds_archives/select"

# Test queries for different rovers
test_queries = [
    {
        "name": "Curiosity (MSL) - Recent Images",
        "params": {
            "q": "mission_name:\"MARS SCIENCE LABORATORY\"",
            "rows": 5,
            "sort": "start_time desc",
            "wt": "json"
        }
    },
    {
        "name": "Perseverance (Mars 2020) - Recent Images",
        "params": {
            "q": "mission_name:\"MARS 2020\"",
            "rows": 5,
            "sort": "start_time desc",
            "wt": "json"
        }
    },
    {
        "name": "All Mars Missions",
        "params": {
            "q": "target_name:MARS",
            "rows": 10,
            "wt": "json",
            "fl": "mission_name,product_id,start_time,instrument_name"
        }
    }
]

print("🔍 Testing PDS Imaging Atlas Search API")
print("=" * 70)
print()

for query in test_queries:
    print(f"📡 Query: {query['name']}")
    print(f"Parameters: {query['params']}")
    print()
    
    try:
        response = requests.get(BASE_URL, params=query['params'], timeout=15)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Show response structure
            print(f"✅ SUCCESS!")
            if 'response' in data:
                num_found = data['response'].get('numFound', 0)
                docs = data['response'].get('docs', [])
                print(f"Total found: {num_found}")
                print(f"Returned: {len(docs)} documents")
                print()
                
                # Show first result details
                if docs:
                    print("First result sample:")
                    first_doc = docs[0]
                    for key, value in list(first_doc.items())[:10]:  # Show first 10 fields
                        print(f"  {key}: {value}")
                    print()
            else:
                print(f"Response keys: {list(data.keys())}")
                print(json.dumps(data, indent=2)[:500])
        else:
            print(f"❌ HTTP Error {response.status_code}")
            print(f"Response: {response.text[:300]}")
            
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
    
    print("-" * 70)
    print()
