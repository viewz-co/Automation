#!/usr/bin/env python3
"""
Environment Setup Script for Playwright Python Framework

This script helps set up environment variables for the testing framework.
It now works with the new centralized environment configuration system.

The framework uses configs/environment.py for smart defaults and multi-environment support.
This script helps you override those defaults when needed.

Usage:
    python setup_env.py
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent))

# Import centralized configuration to show current values
try:
    from configs.environment import get_base_url, get_api_base_url, get_environment_name
    CENTRALIZED_CONFIG_AVAILABLE = True
except ImportError:
    CENTRALIZED_CONFIG_AVAILABLE = False
    print("⚠️ Warning: Centralized config not available, using fallback values")

def show_current_config():
    """Show current configuration from centralized system"""
    print("🔧 Current Configuration:")
    print("=" * 40)
    
    if CENTRALIZED_CONFIG_AVAILABLE:
        print(f"Environment: {get_environment_name()}")
        print(f"Base URL: {get_base_url()}")
        print(f"API Base URL: {get_api_base_url()}")
    else:
        print("Environment: production (fallback)")
        print("Base URL: https://app.viewz.co (fallback)")
        print("API Base URL: https://app.viewz.co (fallback)")
    
    print(f"Username: {os.getenv('TEST_USERNAME', 'Not Set')}")
    print(f"Password: {'***' if os.getenv('TEST_PASSWORD') else 'Not Set'}")
    print(f"OTP Secret: {'***' if os.getenv('TEST_TOTP_SECRET') else 'Not Set'}")
    print()

def setup_environment_variables():
    """Interactive setup of environment variables"""
    print("🚀 Environment Setup for Playwright Python Framework")
    print("=" * 50)
    print()
    
    print("ℹ️  This framework now uses centralized configuration!")
    print("   - Default URLs are managed in configs/environment.py")
    print("   - Environment variables override the smart defaults")
    print("   - Support for multiple environments (dev/staging/prod)")
    print()
    
    show_current_config()
    
    print("📝 Let's set up your environment variables:")
    print("   (Press Enter to keep current values)")
    print()
    
    # Environment selection
    current_env = os.getenv('ENVIRONMENT', 'production')
    print(f"🌍 Environment Selection (current: {current_env})")
    print("   Options: production, staging, development, local")
    new_env = input("   New environment: ").strip()
    if new_env:
        os.environ['ENVIRONMENT'] = new_env
        print(f"   ✅ Environment set to: {new_env}")
    
    # URL overrides (optional)
    print(f"\n🔗 URL Configuration (optional overrides)")
    if CENTRALIZED_CONFIG_AVAILABLE:
        current_base = get_base_url()
        current_api = get_api_base_url()
    else:
        current_base = "https://app.viewz.co"
        current_api = "https://app.viewz.co"
    
    print(f"   Current Base URL: {current_base}")
    new_base = input("   Override Base URL (or press Enter): ").strip()
    if new_base:
        os.environ['BASE_URL'] = new_base
        print(f"   ✅ Base URL override: {new_base}")
    
    print(f"   Current API URL: {current_api}")
    new_api = input("   Override API URL (or press Enter): ").strip()
    if new_api:
        os.environ['API_BASE_URL'] = new_api
        print(f"   ✅ API URL override: {new_api}")
    
    # Required credentials
    print(f"\n🔐 Authentication Credentials (required)")
    
    current_username = os.getenv('TEST_USERNAME', '')
    print(f"   Current Username: {current_username}")
    new_username = input("   Username: ").strip()
    if new_username:
        os.environ['TEST_USERNAME'] = new_username
        print(f"   ✅ Username set")
    
    current_password = os.getenv('TEST_PASSWORD', '')
    password_status = "***" if current_password else "Not Set"
    print(f"   Current Password: {password_status}")
    new_password = input("   Password: ").strip()
    if new_password:
        os.environ['TEST_PASSWORD'] = new_password
        print(f"   ✅ Password set")
    
    current_otp = os.getenv('TEST_TOTP_SECRET', '')
    otp_status = "***" if current_otp else "Not Set"
    print(f"   Current OTP Secret: {otp_status}")
    new_otp = input("   2FA OTP Secret: ").strip()
    if new_otp:
        os.environ['TEST_TOTP_SECRET'] = new_otp
        print(f"   ✅ OTP Secret set")
    
    # Optional configurations
    print(f"\n⚙️  Optional Configuration")
    
    # JWT Token
    current_jwt = os.getenv('JWT_TOKEN', '')
    jwt_status = "***" if current_jwt else "Not Set"
    print(f"   Current JWT Token: {jwt_status}")
    new_jwt = input("   JWT Token (for API tests): ").strip()
    if new_jwt:
        os.environ['JWT_TOKEN'] = new_jwt
        print(f"   ✅ JWT Token set")

def save_to_env_file():
    """Save current environment variables to .env file"""
    env_file_path = Path('.env')
    
    env_vars = [
        'ENVIRONMENT',
        'BASE_URL', 
        'API_BASE_URL',
        'TEST_USERNAME',
        'TEST_PASSWORD', 
        'TEST_TOTP_SECRET',
        'JWT_TOKEN',
        'TESTRAIL_URL',
        'TESTRAIL_USERNAME',
        'TESTRAIL_PASSWORD',
        'TESTRAIL_PROJECT_ID'
    ]
    
    print(f"\n💾 Saving configuration to {env_file_path}")
    
    with open(env_file_path, 'w') as f:
        f.write("# Playwright Python Framework Environment Configuration\n")
        f.write("# Generated by setup_env.py\n")
        f.write("# Uses centralized config from configs/environment.py\n\n")
        
        for var in env_vars:
            value = os.getenv(var, '')
            if value:
                f.write(f"{var}={value}\n")
    
    print(f"✅ Configuration saved to {env_file_path}")
    print("   The framework will use these values to override smart defaults")

def main():
    """Main setup function"""
    setup_environment_variables()
    
    print("\n" + "=" * 50)
    print("📊 Final Configuration Summary:")
    show_current_config()
    
    save_choice = input("💾 Save configuration to .env file? (y/N): ").strip().lower()
    if save_choice in ['y', 'yes']:
        save_to_env_file()
    
    print("\n🎉 Environment setup complete!")
    print("📚 Next steps:")
    print("   1. Run tests: pytest tests/ -v")
    print("   2. Run specific scenario: python scripts/run_login_scenarios.py") 
    print("   3. Check configs/environment.py for available environments")
    print("   4. Switch environments by setting ENVIRONMENT variable")

if __name__ == "__main__":
    main() 