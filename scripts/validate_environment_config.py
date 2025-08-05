#!/usr/bin/env python3
"""
Environment Configuration Validation Script

This script validates and demonstrates the centralized environment configuration system.
It helps ensure that the configuration is working correctly across different environments.

Usage:
    python scripts/validate_environment_config.py
    
    # Test specific environment
    ENVIRONMENT=staging python scripts/validate_environment_config.py
    
    # Test with overrides
    BASE_URL=https://custom.example.com python scripts/validate_environment_config.py
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent))

def test_centralized_config():
    """Test the centralized configuration system"""
    print("🧪 Testing Centralized Environment Configuration")
    print("=" * 50)
    
    try:
        # Import centralized configuration
        from configs.environment import (
            get_base_url, get_api_base_url, get_login_url,
            get_environment_name, get_environment_config,
            is_production, is_local, EnvironmentConfig
        )
        
        print("✅ Successfully imported centralized configuration")
        
        # Test basic functions
        print("\n📋 Current Configuration:")
        print(f"   Environment: {get_environment_name()}")
        print(f"   Base URL: {get_base_url()}")
        print(f"   API Base URL: {get_api_base_url()}")
        print(f"   Login URL: {get_login_url()}")
        print(f"   Is Production: {is_production()}")
        print(f"   Is Local: {is_local()}")
        
        # Test full config
        full_config = get_environment_config()
        print(f"\n🔧 Full Configuration:")
        for key, value in full_config.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing centralized config: {str(e)}")
        return False

def test_environment_switching():
    """Test switching between different environments"""
    print("\n🔄 Testing Environment Switching")
    print("=" * 40)
    
    try:
        from configs.environment import EnvironmentConfig, reload_config
        
        # Test each environment
        environments_to_test = ['production', 'staging', 'development', 'local']
        
        for env in environments_to_test:
            print(f"\n🌍 Testing {env} environment:")
            
            # Set environment variable
            original_env = os.getenv('ENVIRONMENT')
            os.environ['ENVIRONMENT'] = env
            
            # Reload configuration
            reload_config()
            
            # Import fresh config
            from configs.environment import get_base_url, get_environment_name
            
            print(f"   Name: {get_environment_name()}")
            print(f"   URL: {get_base_url()}")
            
            # Restore original environment
            if original_env:
                os.environ['ENVIRONMENT'] = original_env
            else:
                os.environ.pop('ENVIRONMENT', None)
        
        # Reload to restore original state
        reload_config()
        print("\n✅ Environment switching test completed")
        return True
        
    except Exception as e:
        print(f"❌ Error testing environment switching: {str(e)}")
        return False

def test_environment_overrides():
    """Test environment variable overrides"""
    print("\n🔧 Testing Environment Variable Overrides")
    print("=" * 40)
    
    try:
        from configs.environment import get_base_url, reload_config
        
        # Get original URL
        original_url = get_base_url()
        print(f"Original URL: {original_url}")
        
        # Test override
        test_url = "https://test.example.com"
        os.environ['BASE_URL'] = test_url
        
        # Reload configuration
        reload_config()
        
        # Check if override worked
        new_url = get_base_url()
        print(f"Override URL: {new_url}")
        
        if new_url == test_url:
            print("✅ Environment variable override works")
            success = True
        else:
            print("❌ Environment variable override failed")
            success = False
        
        # Clean up
        os.environ.pop('BASE_URL', None)
        reload_config()
        
        restored_url = get_base_url()
        print(f"Restored URL: {restored_url}")
        
        return success
        
    except Exception as e:
        print(f"❌ Error testing environment overrides: {str(e)}")
        return False

def test_secure_config_integration():
    """Test integration with secure config file"""
    print("\n🔒 Testing Secure Config Integration")
    print("=" * 40)
    
    try:
        secure_config_path = Path(__file__).parent.parent / 'configs' / 'env_config_secure.json'
        
        if secure_config_path.exists():
            print(f"✅ Secure config file found: {secure_config_path}")
            
            # Test that it loads without errors
            from configs.environment import get_base_url
            url = get_base_url()
            print(f"   Config loads successfully, URL: {url}")
            
        else:
            print(f"ℹ️  Secure config file not found: {secure_config_path}")
            print("   This is normal - secure config is optional")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing secure config: {str(e)}")
        return False

def show_migration_status():
    """Show status of migration from hardcoded URLs"""
    print("\n📊 Migration Status from Hardcoded URLs")
    print("=" * 40)
    
    # Files that should be using centralized config
    files_to_check = [
        'tests/conftest.py',
        'tests/e2e/login/test_login_scenarios.py', 
        'scripts/run_login_scenarios.py',
        'scripts/mcp_python_client.py',
        'demo_login_scenarios.py'
    ]
    
    migrated_files = []
    needs_migration = []
    
    for file_path in files_to_check:
        full_path = Path(__file__).parent.parent / file_path
        
        if full_path.exists():
            try:
                content = full_path.read_text()
                
                # Check for centralized config imports
                has_centralized_import = (
                    'from configs.environment import' in content or
                    'import configs.environment' in content
                )
                
                # Check for hardcoded URLs
                has_hardcoded_urls = (
                    'https://app.viewz.co' in content or
                    'https://new.viewz.co' in content or
                    'https://staging.viewz.co' in content
                )
                
                if has_centralized_import:
                    migrated_files.append(file_path)
                    status = "✅ Migrated"
                elif has_hardcoded_urls:
                    needs_migration.append(file_path)
                    status = "⚠️ Needs Migration"
                else:
                    status = "ℹ️ No URLs"
                
                print(f"   {status}: {file_path}")
                
            except Exception as e:
                print(f"   ❌ Error reading {file_path}: {str(e)}")
        else:
            print(f"   ❓ Not found: {file_path}")
    
    print(f"\n📈 Migration Summary:")
    print(f"   ✅ Migrated files: {len(migrated_files)}")
    print(f"   ⚠️ Files needing migration: {len(needs_migration)}")
    
    if needs_migration:
        print(f"\n🔧 Files still needing migration:")
        for file_path in needs_migration:
            print(f"   - {file_path}")

def main():
    """Main validation function"""
    print("🚀 Environment Configuration Validation")
    print("=" * 50)
    print(f"Current working directory: {Path.cwd()}")
    print(f"Python path: {sys.path[0]}")
    print()
    
    # Show current environment variables
    print("🌍 Current Environment Variables:")
    env_vars = ['ENVIRONMENT', 'BASE_URL', 'API_BASE_URL']
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"   {var}: {value}")
        else:
            print(f"   {var}: (not set)")
    print()
    
    # Run tests
    tests = [
        ("Basic Configuration", test_centralized_config),
        ("Environment Switching", test_environment_switching), 
        ("Environment Overrides", test_environment_overrides),
        ("Secure Config Integration", test_secure_config_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with exception: {str(e)}")
            results[test_name] = False
    
    # Show migration status
    show_migration_status()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Validation Summary")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}: {test_name}")
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All validation tests passed!")
        print("✅ Centralized environment configuration is working correctly")
    else:
        print("⚠️ Some validation tests failed")
        print("🔧 Please check the configuration and fix any issues")
    
    print("\n📚 Next Steps:")
    print("   1. Run tests with: pytest tests/ -v")
    print("   2. Test different environments: ENVIRONMENT=staging python scripts/validate_environment_config.py")
    print("   3. Override URLs: BASE_URL=https://custom.com python scripts/validate_environment_config.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 