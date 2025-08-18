#!/usr/bin/env python3
"""
Interactive BO Debug
Script that logs into BO and waits for user interaction to show relogin functionality
"""

import asyncio
from playwright.async_api import async_playwright
import json
import pyotp

async def interactive_bo_debug():
    """Login to BO and wait for user to show relogin functionality"""
    
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
            
            # Perform login
            print("🔐 Performing BO login...")
            await page.fill('input[name="userName"]', bo_config['username'])
            await page.fill('input[name="password"]', bo_config['password'])
            await page.click('button[type="submit"]')
            
            # Handle OTP
            await asyncio.sleep(2)
            totp = pyotp.TOTP(bo_config['otp_secret'])
            otp_code = totp.now()
            print(f"🔐 Generated OTP: {otp_code}")
            
            await page.wait_for_selector("text=code", timeout=10000)
            await page.fill('input[type="text"]', otp_code)
            await page.click('button:has-text("Verify")')
            
            await asyncio.sleep(5)
            print("✅ Login completed successfully!")
            
            # Current page info
            url = page.url
            title = await page.title()
            print(f"📄 Current page after login:")
            print(f"   URL: {url}")
            print(f"   Title: {title}")
            
            # Take initial screenshot
            await page.screenshot(path="interactive_bo_logged_in.png")
            print("📸 Screenshot saved: interactive_bo_logged_in.png")
            
            print("\n" + "="*60)
            print("🎯 INTERACTIVE MODE - BROWSER IS NOW OPEN")
            print("="*60)
            print()
            print("The browser is now logged into the BO system and ready for interaction.")
            print("Please navigate to the page where accounts are listed and show me:")
            print("1. Where the accounts are displayed")
            print("2. Where the 'Relogin' button is for each account")
            print("3. Any other relevant elements")
            print()
            print("The browser will stay open for 10 minutes while you explore...")
            print("Press Ctrl+C in the terminal when you're done to close the browser.")
            print()
            print("="*60)
            
            # Wait for a long time to allow manual exploration
            # User can press Ctrl+C to interrupt
            for i in range(600):  # 10 minutes
                await asyncio.sleep(1)
                if i % 60 == 0:  # Every minute
                    current_url = page.url
                    print(f"⏰ Still running... Current URL: {current_url} (Minute {i//60 + 1}/10)")
            
            print("\n⏰ 10 minutes elapsed. Closing browser...")
            
        except KeyboardInterrupt:
            print("\n👋 User interrupted. Saving final state...")
            
            # Save final screenshot and page info
            final_url = page.url
            await page.screenshot(path="interactive_bo_final_state.png")
            print(f"📸 Final screenshot saved: interactive_bo_final_state.png")
            print(f"🔗 Final URL: {final_url}")
            
            # Save page content for analysis
            content = await page.content()
            with open('interactive_bo_final_content.html', 'w') as f:
                f.write(content)
            print("💾 Final page content saved: interactive_bo_final_content.html")
            
        except Exception as e:
            print(f"❌ Error during interactive session: {str(e)}")
            await page.screenshot(path="interactive_bo_error.png")
            
        finally:
            print("🔄 Closing browser...")
            await browser.close()
            print("✅ Browser closed. Session complete!")

if __name__ == "__main__":
    print("🚀 Starting Interactive BO Debug Session")
    print("This will log into BO and keep the browser open for you to explore.")
    print()
    
    try:
        asyncio.run(interactive_bo_debug())
    except KeyboardInterrupt:
        print("\n👋 Session ended by user.")
    except Exception as e:
        print(f"❌ Session error: {str(e)}")
