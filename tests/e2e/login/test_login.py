import os
import asyncio
import pyotp
import pytest
from pages.login_page import LoginPage

@pytest.mark.asyncio
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

