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
    # TOTP Secret (מהאפליקציה שלך - לדוגמה Microsoft Authenticator)
    secret = os.getenv('TEST_TOTP_SECRET')
    otp = pyotp.TOTP(secret).now()
    #otp='492796'

    print("Current OTP:", otp)

    login = LoginPage(page)
    await login.goto()
    await login.login(login_data["username"], login_data["password"])

    # המתן שדה OTP
    await page.wait_for_selector("text=Two-Factor Authentication")
    await page.wait_for_selector("form")
    await page.get_by_role("textbox").fill(otp)
    #await page.click("button[type='verify']")
    await asyncio.sleep(5)

    assert await login.is_logged_in()

