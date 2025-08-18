import os
import asyncio
import pyotp
import pytest
from pages.login_page import LoginPage

def is_valid_credentials():
    """Check if we have valid credentials for testing"""
    username = os.getenv('TEST_USERNAME', '')
    password = os.getenv('TEST_PASSWORD', '')
    secret = os.getenv('TEST_TOTP_SECRET', '')
    
    # Skip if using placeholder values
    if (username in ['test_user_placeholder', 'test_user', ''] or 
        password in ['test_password_placeholder', 'test_pass', ''] or
        secret in ['test_secret', '']):
        return False
        
    # Validate TOTP secret format
    try:
        pyotp.TOTP(secret).now()
        return True
    except Exception:
        return False

@pytest.mark.asyncio
@pytest.mark.skipif(not is_valid_credentials(), reason="Valid credentials not available for authentication test")
async def test_login(page, login_data):
    # TOTP Secret - use from login_data (supports both production and stage)
    secret = login_data.get("otp_secret") or os.getenv('TEST_TOTP_SECRET')
    otp = pyotp.TOTP(secret).now()
    #otp='492796'

    print(f"Current OTP: {otp} (using secret from {login_data.get('environment', 'production')} environment)")

    login = LoginPage(page)
    await login.goto()
    await login.login(login_data["username"], login_data["password"])

    # המתן שדה OTP - flexible 2FA detection
    try:
        await page.wait_for_selector("text=Two-Factor Authentication", timeout=3000)
    except:
        try:
            await page.wait_for_selector("text=Authentication", timeout=2000)
        except:
            try:
                await page.wait_for_selector("text=verification", timeout=2000) 
            except:
                try:
                    await page.wait_for_selector("text=code", timeout=2000)
                except:
                    try:
                        # Check if already logged in
                        await page.wait_for_url("**/home**", timeout=2000)
                        print("✅ Already logged in, skipping 2FA")
                        return  # Already logged in
                    except:
                        print("⚠️ Could not detect 2FA page, attempting OTP anyway")
    
    # Try to find and fill OTP
    try:
        await page.wait_for_selector("form", timeout=2000)
    except:
        pass  # Form might not be detectable
        
    try:
        await page.get_by_role("textbox").fill(otp)
    except:
        try:
            await page.locator('input[type="text"]:visible').last.fill(otp)
        except:
            try:
                await page.locator('input:visible').last.fill(otp)
            except:
                print("⚠️ Could not fill OTP - no suitable input found")
    #await page.click("button[type='verify']")
    await asyncio.sleep(5)

    assert await login.is_logged_in()

