#!/usr/bin/env python3
"""List all TestRail sections to find Credit Card"""

import os
import requests
from base64 import b64encode

url = os.getenv('TESTRAIL_URL', 'https://viewz.testrail.io')
username = os.getenv('TESTRAIL_USERNAME', 'automation@viewz.co')
password = os.getenv('TESTRAIL_PASSWORD', 'e.fJg:z5q5mnAdL')
project_id = 1
suite_id = 4

auth = b64encode(f"{username}:{password}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}

response = requests.get(
    f"{url}/index.php?/api/v2/get_sections/{project_id}&suite_id={suite_id}",
    headers=headers
)

if response.status_code == 200:
    result = response.json()
    sections = result.get('sections', [])
    
    print("\n📁 ALL TESTRAIL SECTIONS IN SUITE 4:\n")
    print("=" * 80)
    
    for section in sections:
        section_id = section.get('id')
        name = section.get('name')
        parent_id = section.get('parent_id')
        depth = section.get('depth', 0)
        
        indent = "  " * depth
        print(f"{indent}[{section_id}] {name}")
        
        if 'credit' in name.lower() or 'card' in name.lower():
            print(f"{indent}     ⭐ POTENTIAL MATCH!")
    
    print("=" * 80)
else:
    print(f"❌ Error: {response.status_code}")

