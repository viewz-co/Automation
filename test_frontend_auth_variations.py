#!/usr/bin/env python3
"""
Test Frontend Authentication Variations
Try different auth endpoints and patterns from the frontend code
"""

import requests
import json
import time
import uuid

def test_frontend_auth_patterns():
    """Test various authentication patterns from the frontend"""
    
    base_url = "https://api.viewz.co/api"
    
    # Generate tab-id like frontend
    tab_id = f"tab-{int(time.time() * 1000)}-{uuid.uuid4().hex[:7]}"
    
    # Test different authentication endpoints from frontend
    auth_endpoints = [
        "/v2/auth/login",
        "/auth/login", 
        "/auth/supportReLogin"
    ]
    
    # Different credential approaches
    credential_sets = [
        {
            "name": "Standard Login",
            "data": {
                "username": "sharon@hoffmanemail.com",
                "password": "12345678"
            }
        },
        {
            "name": "Email Field",
            "data": {
                "email": "sharon@hoffmanemail.com", 
                "password": "12345678"
            }
        },
        {
            "name": "Different Password",
            "data": {
                "username": "sharon@hoffmanemail.com",
                "password": "Password123"
            }
        },
        {
            "name": "Demo Account", 
            "data": {
                "username": "demo@viewz.co",
                "password": "demo123"
            }
        }
    ]
    
    print("=" * 80)
    print("TESTING FRONTEND AUTHENTICATION PATTERNS")
    print("=" * 80)
    
    for endpoint in auth_endpoints:
        print(f"\n🔗 Testing endpoint: {base_url}{endpoint}")
        print("-" * 60)
        
        for cred_set in credential_sets:
            print(f"\n📝 {cred_set['name']}")
            
            # Create session with frontend headers
            session = requests.Session()
            session.headers.update({
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'tab-id': tab_id,
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            
            try:
                url = f"{base_url}{endpoint}"
                print(f"   URL: {url}")
                print(f"   Data: {json.dumps(cred_set['data'], indent=6)}")
                
                response = session.post(url, json=cred_set['data'], timeout=10)
                
                print(f"   Status: {response.status_code}")
                print(f"   Headers: {dict(response.headers)}")
                print(f"   Response: {response.text[:400]}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if (data.get('result') == 'SUCCESS' or 
                            'jwToken' in data or 
                            'jwtToken' in data or
                            data.get('data', {}).get('jwToken')):
                            print(f"   ✅ POTENTIAL SUCCESS!")
                            print(f"   JWT Token: {data.get('jwToken') or data.get('jwtToken') or data.get('data', {}).get('jwToken', 'Not found')}")
                            print(f"   Full response: {json.dumps(data, indent=6)}")
                            return True, cred_set, endpoint, data
                        elif data.get('result') == 'OTP_REQUIRED':
                            print(f"   🔐 OTP REQUIRED - Login successful, needs 2FA")
                        else:
                            print(f"   ❌ Login failed: {data.get('message', 'Unknown error')}")
                    except json.JSONDecodeError:
                        print(f"   ⚠️  Non-JSON response")
                        
                elif response.status_code in [301, 302, 303, 307, 308]:
                    print(f"   🔄 Redirect to: {response.headers.get('Location', 'Unknown')}")
                    
                else:
                    print(f"   ❌ HTTP Error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    print(f"\n❌ No working authentication found")
    return False, None, None, None

def test_getUserInfo_endpoints():
    """Test if we can access getUserInfo endpoints without auth (discovery)"""
    
    print(f"\n" + "=" * 80)
    print("TESTING DISCOVERY ENDPOINTS")
    print("=" * 80)
    
    base_url = "https://api.viewz.co/api"
    tab_id = f"tab-{int(time.time() * 1000)}-{uuid.uuid4().hex[:7]}"
    
    endpoints_to_test = [
        "/v2/auth/getUserInfo",
        "/auth/getUserInfo", 
        "/v2/userGroups/getUserGroupDashboards",
        "/entities/getUserGroupEntities"
    ]
    
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'tab-id': tab_id
    })
    
    for endpoint in endpoints_to_test:
        url = f"{base_url}{endpoint}"
        try:
            response = session.get(url, timeout=5)
            print(f"{endpoint:<40} {response.status_code} ({len(response.text)} chars)")
            
            if response.status_code not in [401, 403, 404]:
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=3)[:200]}...")
                except:
                    print(f"   Text: {response.text[:100]}...")
                    
        except Exception as e:
            print(f"{endpoint:<40} ❌ {str(e)[:30]}...")

if __name__ == "__main__":
    success, working_creds, working_endpoint, auth_data = test_frontend_auth_patterns()
    
    if success:
        print(f"\n🎉 SUCCESS! Found working authentication:")
        print(f"   Endpoint: {working_endpoint}")
        print(f"   Credentials: {working_creds}")
        print(f"   Auth Response: {json.dumps(auth_data, indent=2)}")
    else:
        test_getUserInfo_endpoints()
        print(f"\n💡 Next steps:")
        print(f"   1. Verify credentials with system administrator")
        print(f"   2. Check if account needs to be activated")
        print(f"   3. Try different credential combinations")
        print(f"   4. Continue with mock mode for testing") 