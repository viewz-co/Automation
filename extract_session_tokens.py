#!/usr/bin/env python3
"""
Extract Session Storage Tokens
Extract jwtToken, appSessionId, and tabId from browser session storage
"""

import asyncio
import json
from playwright.async_api import async_playwright

async def extract_session_tokens():
    """Extract session storage tokens from an authenticated browser session"""
    
    print("=" * 80)
    print("EXTRACTING SESSION STORAGE TOKENS FROM BROWSER")
    print("=" * 80)
    
    async with async_playwright() as p:
        # Launch browser with visible UI for manual login
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to the login page
            print("🌐 Navigating to Viewz login page...")
            await page.goto("https://new.viewz.co/login")
            await page.wait_for_load_state("networkidle")
            
            print("\n🔐 Please complete the login process manually in the browser:")
            print("   1. Enter your username and password")
            print("   2. Complete 2FA/OTP if required")
            print("   3. Wait until you reach the dashboard")
            print("   4. Press ENTER here when logged in successfully...")
            
            # Wait for user to complete login
            input("\nPress ENTER after successful login: ")
            
            # Extract session storage values
            print("\n📦 Extracting session storage values...")
            
            # Get all session storage items
            session_storage = await page.evaluate("""
                () => {
                    const storage = {};
                    for (let i = 0; i < sessionStorage.length; i++) {
                        const key = sessionStorage.key(i);
                        storage[key] = sessionStorage.getItem(key);
                    }
                    return storage;
                }
            """)
            
            # Get specific tokens we need
            jwt_token = await page.evaluate("() => sessionStorage.getItem('jwtToken')")
            app_session_id = await page.evaluate("() => sessionStorage.getItem('appSessionId')")
            tab_id = await page.evaluate("() => sessionStorage.getItem('tabId')")
            
            print(f"\n✅ Session Storage Contents:")
            print(f"   📋 All items: {len(session_storage)} total")
            for key, value in session_storage.items():
                value_display = value[:50] + "..." if value and len(value) > 50 else value
                print(f"      {key}: {value_display}")
            
            print(f"\n🔑 Key Authentication Tokens:")
            print(f"   JWT Token: {jwt_token[:50] + '...' if jwt_token else 'NOT FOUND'}")
            print(f"   App Session ID: {app_session_id or 'NOT FOUND'}")
            print(f"   Tab ID: {tab_id or 'NOT FOUND'}")
            
            # Save tokens to file for use in tests
            if jwt_token:
                tokens = {
                    "jwtToken": jwt_token,
                    "appSessionId": app_session_id,
                    "tabId": tab_id,
                    "extractedAt": str(asyncio.get_event_loop().time())
                }
                
                with open("extracted_tokens.json", "w") as f:
                    json.dump(tokens, f, indent=2)
                
                print(f"\n💾 Tokens saved to 'extracted_tokens.json'")
                return tokens
            else:
                print(f"\n❌ No JWT token found. Make sure you're fully logged in.")
                return None
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            # Keep browser open for a moment
            print(f"\n⏳ Keeping browser open for 5 seconds...")
            await asyncio.sleep(5)
            await browser.close()

async def test_extracted_tokens():
    """Test the extracted tokens with our API client"""
    
    print(f"\n" + "=" * 80)
    print("TESTING EXTRACTED TOKENS")
    print("=" * 80)
    
    try:
        with open("extracted_tokens.json", "r") as f:
            tokens = json.load(f)
        
        print(f"📂 Loaded tokens from file:")
        print(f"   JWT Token: {tokens.get('jwtToken', 'Missing')[:50]}...")
        print(f"   App Session ID: {tokens.get('appSessionId', 'Missing')}")
        print(f"   Tab ID: {tokens.get('tabId', 'Missing')}")
        
        # Test with our API client
        from api.api_client import APIClient
        
        client = APIClient(base_url="https://api.viewz.co/api")
        
        # Set the extracted tokens
        if tokens.get('jwtToken'):
            client.set_authentication(
                tokens['jwtToken'],
                tokens.get('appSessionId'),
                None  # entity_id not needed for basic tests
            )
            
            # Override tab-id header
            if tokens.get('tabId'):
                client.session.headers['tab-id'] = tokens['tabId']
            
            print(f"\n🧪 Testing API call with extracted tokens...")
            
            # Try a simple API call
            try:
                response = client.get('/v2/auth/getUserInfo')
                print(f"   ✅ API call successful!")
                print(f"   Response: {response}")
                return True
                
            except Exception as e:
                print(f"   ❌ API call failed: {e}")
                
                # Try another endpoint
                try:
                    response = client.get('/v2/accounting/getJournalEntries')
                    print(f"   ✅ Journal entries call successful!")
                    print(f"   Response: {response}")
                    return True
                except Exception as e2:
                    print(f"   ❌ Journal entries call also failed: {e2}")
                    return False
        else:
            print(f"   ❌ No JWT token available for testing")
            return False
            
    except FileNotFoundError:
        print(f"   ❌ No extracted tokens file found. Run extraction first.")
        return False
    except Exception as e:
        print(f"   ❌ Error testing tokens: {e}")
        return False

async def main():
    """Main function to extract and test tokens"""
    
    print("🎯 SESSION TOKEN EXTRACTION AND TESTING")
    print("This script will help you extract real session tokens from the browser")
    print("and test them with our API client.\n")
    
    # Step 1: Extract tokens
    tokens = await extract_session_tokens()
    
    if tokens:
        # Step 2: Test tokens
        success = await test_extracted_tokens()
        
        if success:
            print(f"\n🎉 SUCCESS! Real API authentication working!")
            print(f"   You can now update your config with these tokens")
            print(f"   Or use the extracted_tokens.json file for testing")
        else:
            print(f"\n⚠️  Tokens extracted but API calls still failing")
            print(f"   This might be due to API endpoint or permission issues")
    else:
        print(f"\n❌ Token extraction failed")
        print(f"   Make sure you complete the full login process")

if __name__ == "__main__":
    asyncio.run(main()) 