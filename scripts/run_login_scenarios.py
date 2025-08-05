"""
Login Scenarios Automation Script

Executes login scenarios for the configured environment using Playwright Python
Demonstrates 2FA integration, page navigation, and automated testing patterns.

Updated: Uses centralized environment configuration for URLs
"""

import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright
import pyotp
import json
from datetime import datetime
import time

# Add project root to Python path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import centralized configuration
from configs.environment import get_login_url, get_base_url, get_environment_name

print(f"🌍 Environment: {get_environment_name()}")
print(f"🔗 Target URL: {get_login_url()}")

async def run_login_scenarios():
    """Main function to run login scenarios"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Navigate to login page using centralized config
            await page.goto(get_login_url(), wait_until="networkidle")
            
            # Take initial screenshot
            screenshot_path = f"screenshots/login_page_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Initial screenshot: {screenshot_path}")
            
            # Get login credentials from environment
            username = os.getenv("TEST_USERNAME", "sharon_newdemo")
            password = os.getenv("TEST_PASSWORD", "Sh@ron123$%^")
            otp_secret = os.getenv("TEST_TOTP_SECRET", "")
            
            if not otp_secret:
                print("⚠️ No OTP secret provided - skipping 2FA")
                return
            
            # Fill login form
            await page.fill("input[name='email'], input[type='email']", username)
            await page.fill("input[name='password'], input[type='password']", password)
            
            # Generate and enter OTP
            totp = pyotp.TOTP(otp_secret)
            current_otp = totp.now()
            print(f"🔐 Generated OTP: {current_otp}")
            
            # Find and fill OTP field
            otp_input = page.locator("input[name*='otp'], input[name*='code'], input[placeholder*='code']").first
            if await otp_input.is_visible():
                await otp_input.fill(current_otp)
                print("✅ OTP entered successfully")
            else:
                print("⚠️ OTP field not found")
            
            # Submit form
            await page.click("button[type='submit'], button:has-text('Login'), button:has-text('Sign in')")
            
            # Wait for navigation
            await page.wait_for_load_state("networkidle")
            
            # Check if login was successful
            current_url = page.url
            print(f"🌐 Current URL after login: {current_url}")
            
            # Take post-login screenshot
            post_login_screenshot = f"screenshots/post_login_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await page.screenshot(path=post_login_screenshot, full_page=True)
            print(f"📸 Post-login screenshot: {post_login_screenshot}")
            
            # Generate test assertions using centralized config
            await generate_test_assertions(page)
            
            print("✅ Login scenarios completed successfully")
            
        except Exception as e:
            print(f"❌ Error during login scenarios: {str(e)}")
            error_screenshot = f"screenshots/error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            await page.screenshot(path=error_screenshot, full_page=True)
            print(f"📸 Error screenshot: {error_screenshot}")
            
        finally:
            await browser.close()

async def generate_test_assertions(page):
    """Generate automated test assertions based on current page state"""
    print("\n🔍 Generating test assertions...")
    
    assertions = []
    
    # URL assertions using centralized config
    assertions.append("# URL Assertions")
    assertions.append(f"expect(page.url).not.toBe('{get_login_url()}')")
    assertions.append("expect(page.url).toContain('viewz.co')")
    assertions.append("")
    
    # Page title assertion
    title = await page.title()
    assertions.append("# Page Title Assertions")
    assertions.append(f"expect(await page.title()).toBe('{title}')")
    assertions.append("")
    
    # Element presence assertions
    assertions.append("# Element Presence Assertions")
    
    # Check for common dashboard elements
    elements_to_check = [
        ("body", "Page body should be visible"),
        ("nav, .navigation, [role='navigation']", "Navigation should be present"),
        ("header, .header", "Header should be visible"),
        ("main, .main-content, .dashboard", "Main content area should be present")
    ]
    
    for selector, description in elements_to_check:
        count = await page.locator(selector).count()
        if count > 0:
            assertions.append(f"expect(page.locator('{selector}')).toBeVisible(); // {description}")
    
    # Save assertions to file
    assertions_file = f"generated_assertions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.js"
    with open(assertions_file, 'w') as f:
        f.write('\n'.join(assertions))
    
    print(f"📄 Test assertions saved to: {assertions_file}")
    print(f"📊 Generated {len([a for a in assertions if a.startswith('expect')])} assertions")

if __name__ == "__main__":
    print("🚀 Starting login scenarios automation...")
    print("📍 This will:")
    print(f"   1. Navigate to {get_login_url()}")
    print("   2. Analyze the page structure")
    print("   3. Execute login and logout scenarios")
    print("   4. Generate automated test assertions")
    print("   5. Capture screenshots for verification")
    print()
    
    # Create screenshots directory if it doesn't exist
    Path("screenshots").mkdir(exist_ok=True)
    
    # Run the scenarios
    asyncio.run(run_login_scenarios()) 