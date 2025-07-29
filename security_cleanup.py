#!/usr/bin/env python3
"""
Security Cleanup Script
Removes hardcoded secrets from codebase and replaces with environment variables
"""
import os
import re
import json
from pathlib import Path

# Exposed secrets that need to be replaced
EXPOSED_SECRETS = {
    os.getenv('TEST_TOTP_SECRET'): "os.getenv('TEST_TOTP_SECRET')",
    os.getenv('TEST_PASSWORD'): "os.getenv('TEST_PASSWORD')",
    os.getenv('TEST_USERNAME'): "os.getenv('TEST_USERNAME')",
    os.getenv('JWT_TOKEN'): "os.getenv('JWT_TOKEN')"
}

def scan_file_for_secrets(file_path):
    """Scan a file for exposed secrets"""
    secrets_found = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for secret, replacement in EXPOSED_SECRETS.items():
                if secret in content:
                    secrets_found.append((secret, replacement))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return secrets_found

def replace_secrets_in_file(file_path, secrets_found):
    """Replace secrets in a file with environment variable calls"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        modified = False
        for secret, replacement in secrets_found:
            if secret in content:
                # Add import os if not present
                if 'import os' not in content and 'os.getenv' in replacement:
                    content = 'import os\n' + content
                
                # Replace the secret
                content = content.replace(f'"{secret}"', replacement)
                content = content.replace(f"'{secret}'", replacement)
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"Error modifying {file_path}: {e}")
    return False

def scan_repository():
    """Scan the entire repository for exposed secrets"""
    print("🔍 Scanning repository for exposed secrets...")
    
    # File patterns to scan
    patterns = ['*.py', '*.json', '*.txt', '*.md', '*.yml', '*.yaml']
    
    # Directories to skip
    skip_dirs = {'.git', '__pycache__', 'venv', 'node_modules', '.pytest_cache'}
    
    affected_files = {}
    
    for pattern in patterns:
        for file_path in Path('.').rglob(pattern):
            # Skip if in excluded directory
            if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                continue
                
            secrets_found = scan_file_for_secrets(file_path)
            if secrets_found:
                affected_files[str(file_path)] = secrets_found
    
    return affected_files

def create_secure_config():
    """Create a secure configuration template"""
    secure_config = {
        "base_url": "https://app.viewz.co",
        "username": "${TEST_USERNAME}",
        "password": "${TEST_PASSWORD}",
        "otp_secret": "${TEST_TOTP_SECRET}",
        "jwt_token": "${JWT_TOKEN}"
    }
    
    with open('configs/env_config_secure.json', 'w') as f:
        json.dump(secure_config, f, indent=2)
    
    print("✅ Created secure config template at configs/env_config_secure.json")

def main():
    print("🚨 SECURITY CLEANUP TOOL")
    print("=" * 50)
    
    # Scan for secrets
    affected_files = scan_repository()
    
    if not affected_files:
        print("✅ No exposed secrets found!")
        return
    
    print(f"❌ Found exposed secrets in {len(affected_files)} files:")
    for file_path, secrets in affected_files.items():
        print(f"   📁 {file_path}")
        for secret, _ in secrets:
            print(f"      🔑 {secret[:20]}...")
    
    print("\n🔧 RECOMMENDED ACTIONS:")
    print("1. Change all exposed passwords on target systems")
    print("2. Regenerate TOTP secrets")
    print("3. Invalidate exposed JWT tokens")
    print("4. Create .env file with new secrets")
    print("5. Remove sensitive files from git history")
    
    # Ask user if they want to proceed with replacement
    response = input("\n⚠️  Do you want to replace secrets with env vars? (y/N): ")
    if response.lower() == 'y':
        for file_path, secrets in affected_files.items():
            if replace_secrets_in_file(file_path, secrets):
                print(f"✅ Updated {file_path}")
    
    # Create secure config
    create_secure_config()
    
    print("\n🔒 NEXT STEPS:")
    print("1. Create .env file using env_template.txt")
    print("2. Add new, secure secrets to .env")
    print("3. Test the application")
    print("4. Remove git history: git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch configs/env_config.json' --prune-empty --tag-name-filter cat -- --all")

if __name__ == "__main__":
    main() 