# Stage Environment Setup Guide

## Overview

The framework now supports both **Production** and **Stage** environments for comprehensive testing across different deployment stages.

## Environment Configuration

### Stage Environment URLs
- **Main App**: `https://app.stage.viewz.co`
- **BO (Back Office)**: `https://bo.stage.viewz.co`

### Stage Credentials

#### Main App Stage (`https://app.stage.viewz.co`)
- **Username**: `sharon_stage`
- **Password**: `Fuckyou43!`
- **OTP Secret**: `F44VIIZ6FFLVUVCEIZHVAI2FIRZUWSCS`

#### BO Stage (`https://bo.stage.viewz.co`)
- **Username**: `sharonadmin`
- **Password**: `$h@r0n1#02#`
- **OTP Secret**: `ME2DIJTWJNSGEOJSKJDUI6LSNY3SC2C3`

## Configuration Files

### Main App Stage Configuration
**File**: `configs/stage_env_config.json`
```json
{
  "base_url": "https://app.stage.viewz.co",
  "username": "sharon_stage",
  "password": "Fuckyou43!",
  "otp_secret": "F44VIIZ6FFLVUVCEIZHVAI2FIRZUWSCS",
  "jwt_token": "${JWT_TOKEN}",
  "environment": "stage"
}
```

### BO Stage Configuration
**File**: `configs/bo_stage_env_config.json`
```json
{
  "base_url": "https://bo.stage.viewz.co",
  "username": "sharonadmin", 
  "password": "$h@r0n1#02#",
  "otp_secret": "ME2DIJTWJNSGEOJSKJDUI6LSNY3SC2C3",
  "environment": "stage"
}
```

## Environment Selection

### Using Environment Variable
Set the `TEST_ENV` environment variable to control which environment to use:

```bash
# For Production (default)
export TEST_ENV=production

# For Stage
export TEST_ENV=stage
```

### Automatic Configuration Loading
The framework automatically loads the appropriate configuration based on `TEST_ENV`:

- **Production**: Uses environment variables or production config files
- **Stage**: Uses stage-specific JSON configuration files

## Test Runners

### Main App Stage Tests
**Script**: `run_stage_tests.py`

```bash
# Run all stage tests
python3 run_stage_tests.py all

# Run specific test categories
python3 run_stage_tests.py login
python3 run_stage_tests.py navigation
python3 run_stage_tests.py payables
python3 run_stage_tests.py ledger
python3 run_stage_tests.py reconciliation
python3 run_stage_tests.py performance
python3 run_stage_tests.py snapshot
python3 run_stage_tests.py bo
python3 run_stage_tests.py quick
```

### BO Stage Tests
**Script**: `run_bo_stage_tests.py`

```bash
# Run essential BO stage tests
python3 run_bo_stage_tests.py quick

# Run specific BO test types
python3 run_bo_stage_tests.py complete
python3 run_bo_stage_tests.py login
python3 run_bo_stage_tests.py accounts
python3 run_bo_stage_tests.py relogin
python3 run_bo_stage_tests.py sanity
python3 run_bo_stage_tests.py snapshots
python3 run_bo_stage_tests.py all
```

## Manual Environment Selection

### Using pytest directly with stage environment
```bash
# Set environment and run tests
export TEST_ENV=stage
export TESTRAIL_ENABLED=true
export TESTRAIL_URL=https://viewz.testrail.io
export TESTRAIL_USERNAME=automation@viewz.co
export TESTRAIL_PASSWORD='e.fJg:z5q5mnAdL'

# Run specific tests
python3 -m pytest tests/e2e/login/ -v -s --tb=short
```

## TestRail Integration

TestRail integration remains **the same for both environments**:
- **URL**: `https://viewz.testrail.io`
- **Username**: `automation@viewz.co`
- **Password**: `e.fJg:z5q5mnAdL`

Test results from both production and stage environments are reported to the same TestRail instance.

## Framework Changes

### Updated Files

1. **`tests/conftest.py`**
   - Added environment detection logic
   - Automatic stage configuration loading
   - Maintains backward compatibility with production

2. **`tests/e2e/bo/conftest.py`**
   - BO-specific environment selection
   - Dynamic configuration path selection

3. **Test Runners**
   - `run_stage_tests.py` - Main app stage tests
   - `run_bo_stage_tests.py` - BO stage tests

## Known Issues

### Stage Environment Access
- **Main App Stage**: Currently experiencing `net::ERR_INVALID_AUTH_CREDENTIALS` when accessing `https://app.stage.viewz.co/login`
  - This may indicate HTTP basic authentication is required
  - Or the stage environment may not be publicly accessible
  
- **BO Stage**: Configuration loads correctly, but may redirect to production environment during login flow

### Recommendations
1. **Verify stage environment accessibility** - Ensure stage URLs are accessible from test environment
2. **Check authentication requirements** - Stage may require additional authentication layers
3. **Network configuration** - Verify firewall/VPN requirements for stage access

## Usage Examples

### Quick Stage Test
```bash
# Test stage environment quickly
python3 run_stage_tests.py quick
```

### Full BO Stage Workflow
```bash
# Test complete BO stage workflow
python3 run_bo_stage_tests.py complete
```

### Environment Comparison
```bash
# Run same tests on both environments
export TEST_ENV=production && python3 run_bo_tests.py login
export TEST_ENV=stage && python3 run_bo_stage_tests.py login
```

## Benefits

1. **Environment Isolation**: Test against stage before production deployment
2. **Configuration Management**: Centralized environment-specific settings
3. **Flexible Testing**: Easy switching between environments
4. **CI/CD Ready**: Environment variable-based configuration
5. **TestRail Integration**: Unified reporting across environments

## Next Steps

1. **Resolve stage environment access issues**
2. **Add environment-specific test data**
3. **Implement environment comparison reports**
4. **Add stage-specific test scenarios**
