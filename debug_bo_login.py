#!/usr/bin/env python3
"""
Debug BO Login Page
Simple script to inspect the BO login page structure
"""

import asyncio
from playwright.async_api import async_playwright
import json

async def debug_bo_login_page():
    """Debug the BO login page to understand its structure"""
    
    # Load BO config
    with open('configs/bo_env_config.json', 'r') as f:
        bo_config = json.load(f)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print(f"🌐 Navigating to BO login page: {bo_config['base_url']}/login")
            await page.goto(f"{bo_config['base_url']}/login")
            await page.wait_for_load_state("networkidle")
            
            # Take screenshot
            await page.screenshot(path="debug_bo_login_page.png")
            print("📸 Screenshot saved: debug_bo_login_page.png")
            
            # Check page title
            title = await page.title()
            print(f"📄 Page title: {title}")
            
            # Check URL
            url = page.url
            print(f"🔗 Current URL: {url}")
            
            # Wait a bit to see the page
            await asyncio.sleep(3)
            
            # Find all input elements
            print("\n🔍 Finding all input elements:")
            inputs = await page.locator('input').all()
            for i, input_elem in enumerate(inputs):
                try:
                    input_type = await input_elem.get_attribute('type')
                    input_name = await input_elem.get_attribute('name')
                    input_placeholder = await input_elem.get_attribute('placeholder')
                    input_id = await input_elem.get_attribute('id')
                    input_class = await input_elem.get_attribute('class')
                    
                    print(f"  Input {i+1}:")
                    print(f"    Type: {input_type}")
                    print(f"    Name: {input_name}")
                    print(f"    Placeholder: {input_placeholder}")
                    print(f"    ID: {input_id}")
                    print(f"    Class: {input_class}")
                    print()
                except Exception as e:
                    print(f"    Error getting attributes: {str(e)}")
            
            # Find all button elements
            print("\n🔍 Finding all button elements:")
            buttons = await page.locator('button').all()
            for i, button_elem in enumerate(buttons):
                try:
                    button_type = await button_elem.get_attribute('type')
                    button_text = await button_elem.text_content()
                    button_class = await button_elem.get_attribute('class')
                    
                    print(f"  Button {i+1}:")
                    print(f"    Type: {button_type}")
                    print(f"    Text: {button_text}")
                    print(f"    Class: {button_class}")
                    print()
                except Exception as e:
                    print(f"    Error getting attributes: {str(e)}")
            
            # Get page content for further analysis
            content = await page.content()
            with open('debug_bo_page_content.html', 'w') as f:
                f.write(content)
            print("💾 Page content saved: debug_bo_page_content.html")
            
            # Wait to keep browser open for inspection
            print("\n⏸️  Browser will stay open for 30 seconds for manual inspection...")
            await asyncio.sleep(30)
            
        except Exception as e:
            print(f"❌ Error during debug: {str(e)}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(debug_bo_login_page())
