"""
Centralized Environment Configuration
=====================================

Single source of truth for environment URLs and configuration settings.
Supports multiple environments (dev/staging/production) with fallback defaults.

Usage:
    from configs.environment import get_base_url, get_api_base_url, get_environment_config
    
    # Get current environment URL
    base_url = get_base_url()
    
    # Get full environment configuration
    config = get_environment_config()
"""

import os
from typing import Dict, Any, Optional
from pathlib import Path
import json


class EnvironmentConfig:
    """Centralized environment configuration management"""
    
    # Default environment URLs
    DEFAULT_ENVIRONMENTS = {
        'production': {
            'base_url': 'https://app.viewz.co',
            'api_base_url': 'https://app.viewz.co',
            'name': 'Production',
            'description': 'Production environment'
        },
        'staging': {
            'base_url': 'https://staging.viewz.co',
            'api_base_url': 'https://staging.viewz.co',
            'name': 'Staging',
            'description': 'Staging environment for testing'
        },
        'development': {
            'base_url': 'https://dev.viewz.co',
            'api_base_url': 'https://dev.viewz.co',
            'name': 'Development',
            'description': 'Development environment'
        },
        'local': {
            'base_url': 'http://localhost:3000',
            'api_base_url': 'http://localhost:3001',
            'name': 'Local',
            'description': 'Local development environment'
        }
    }
    
    def __init__(self):
        self._config_cache: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """Load configuration from environment variables and files"""
        # Get current environment (default to production)
        self.current_environment = os.getenv('ENVIRONMENT', 'production').lower()
        
        # Load base configuration from defaults
        if self.current_environment in self.DEFAULT_ENVIRONMENTS:
            self._config_cache = self.DEFAULT_ENVIRONMENTS[self.current_environment].copy()
        else:
            # Fallback to production if unknown environment
            self._config_cache = self.DEFAULT_ENVIRONMENTS['production'].copy()
        
        # Override with environment variables if provided
        self._config_cache.update({
            'base_url': os.getenv('BASE_URL', self._config_cache['base_url']),
            'api_base_url': os.getenv('API_BASE_URL', self._config_cache['api_base_url']),
            'environment': self.current_environment
        })
        
        # Load additional configuration from secure config file if exists
        self._load_secure_config()
    
    def _load_secure_config(self):
        """Load configuration from secure config file"""
        secure_config_path = Path(__file__).parent / 'env_config_secure.json'
        if secure_config_path.exists():
            try:
                with open(secure_config_path, 'r') as f:
                    secure_config = json.load(f)
                    # Only override if not already set by environment variables
                    if 'BASE_URL' not in os.environ and 'base_url' in secure_config:
                        self._config_cache['base_url'] = secure_config['base_url']
                    if 'API_BASE_URL' not in os.environ and 'api_base_url' in secure_config:
                        self._config_cache['api_base_url'] = secure_config['api_base_url']
            except (json.JSONDecodeError, KeyError) as e:
                # In CI environments, this is expected and not an error
                if not self._is_ci_environment():
                    print(f"⚠️ Warning: Could not load secure config: {e}")
    
    def _is_ci_environment(self) -> bool:
        """Check if running in a CI environment"""
        ci_indicators = ['CI', 'GITHUB_ACTIONS', 'JENKINS_URL', 'TRAVIS', 'CIRCLECI']
        return any(os.getenv(indicator) for indicator in ci_indicators)
    
    def get_base_url(self) -> str:
        """Get the base URL for the current environment"""
        return self._config_cache['base_url']
    
    def get_api_base_url(self) -> str:
        """Get the API base URL for the current environment"""
        return self._config_cache['api_base_url']
    
    def get_login_url(self) -> str:
        """Get the full login URL for the current environment"""
        return f"{self.get_base_url()}/login"
    
    def get_environment_name(self) -> str:
        """Get the human-readable environment name"""
        return self._config_cache.get('name', self.current_environment.title())
    
    def get_environment_description(self) -> str:
        """Get the environment description"""
        return self._config_cache.get('description', f'{self.current_environment} environment')
    
    def get_full_config(self) -> Dict[str, Any]:
        """Get the complete configuration dictionary"""
        return self._config_cache.copy()
    
    def is_production(self) -> bool:
        """Check if current environment is production"""
        return self.current_environment == 'production'
    
    def is_local(self) -> bool:
        """Check if current environment is local"""
        return self.current_environment == 'local'
    
    def reload(self):
        """Reload configuration (useful for tests or environment changes)"""
        self._load_config()


# Global configuration instance
_env_config = EnvironmentConfig()

# Convenience functions for easy access
def get_base_url() -> str:
    """Get the base URL for the current environment"""
    return _env_config.get_base_url()

def get_api_base_url() -> str:
    """Get the API base URL for the current environment"""
    return _env_config.get_api_base_url()

def get_login_url() -> str:
    """Get the login URL for the current environment"""
    return _env_config.get_login_url()

def get_environment_name() -> str:
    """Get the human-readable environment name"""
    return _env_config.get_environment_name()

def get_environment_config() -> Dict[str, Any]:
    """Get the complete environment configuration"""
    return _env_config.get_full_config()

def is_production() -> bool:
    """Check if current environment is production"""
    return _env_config.is_production()

def is_local() -> bool:
    """Check if current environment is local"""
    return _env_config.is_local()

def reload_config():
    """Reload configuration from environment variables"""
    _env_config.reload()


# Export the main functions
__all__ = [
    'get_base_url',
    'get_api_base_url', 
    'get_login_url',
    'get_environment_name',
    'get_environment_config',
    'is_production',
    'is_local',
    'reload_config',
    'EnvironmentConfig'
] 