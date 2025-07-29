#!/usr/bin/env python3
"""
Environment Setup Script
Creates .env file with new secure credentials
"""
import os
import secrets
import string

def generate_secure_password(length=16):
    """Generate a secure password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_totp_secret():
    """Generate a new TOTP secret (32 characters, base32)"""
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def create_env_file():
    """Create .env file with secure credentials"""
    
    print("🔐 CREATING SECURE ENVIRONMENT FILE")
    print("=" * 50)
    
    env_content = f"""# SECURE ENVIRONMENT CONFIGURATION
# Generated on: {os.popen('date').read().strip()}
# All credentials below are NEW and secure

# Test Environment
ENV=dev

# Application URLs  
BASE_URL=https://app.viewz.co

# NEW SECURE TEST CREDENTIALS
TEST_USERNAME=sharon_newdemo_secure
TEST_PASSWORD={generate_secure_password(20)}
TEST_TOTP_SECRET={generate_totp_secret()}

# TestRail Integration
TESTRAIL_ENABLED=true
TESTRAIL_URL=https://viewz.testrail.io
TESTRAIL_USERNAME=your_testrail_email@domain.com
TESTRAIL_PASSWORD=your_testrail_api_key
TESTRAIL_PROJECT_ID=1

# API Configuration
API_BASE_URL=https://app.viewz.co
JWT_TOKEN=WILL_BE_GENERATED_AFTER_LOGIN

# SECURITY NOTES:
# 1. This file is ignored by git (.gitignore)
# 2. Update these credentials in your target system
# 3. The TOTP secret must be configured in your 2FA app
# 4. JWT token will be generated after successful login
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Created .env file with secure credentials")
    print("\n🚨 IMPORTANT NEXT STEPS:")
    print("1. Update the target system with the new username/password")
    print("2. Configure the new TOTP secret in your 2FA app") 
    print("3. Update any TestRail API credentials")
    print("4. Test login with new credentials")
    print("\n⚠️  The old credentials MUST be changed in the target system!")

if __name__ == "__main__":
    create_env_file() 