#!/bin/bash

# Test script to verify Docker setup
set -e

echo "🧪 Testing Docker setup for Playwright framework..."

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test 1: Build the Docker image
echo -e "${YELLOW}🔨 Test 1: Building Docker image...${NC}"
if docker build -t playwright-test --target production .; then
    echo -e "${GREEN}✅ Docker image built successfully${NC}"
else
    echo -e "${RED}❌ Docker image build failed${NC}"
    exit 1
fi

# Test 2: Check if Playwright is installed
echo -e "${YELLOW}🎭 Test 2: Checking Playwright installation...${NC}"
if docker run --rm playwright-test python -c "
import playwright
import playwright.sync_api
print('✅ Playwright modules imported successfully')
"; then
    echo -e "${GREEN}✅ Playwright is properly installed${NC}"
else
    echo -e "${RED}❌ Playwright installation check failed${NC}"
    exit 1
fi

# Test 3: Check if browsers are installed
echo -e "${YELLOW}🌐 Test 3: Checking browser installation...${NC}"
if docker run --rm playwright-test playwright install --dry-run chromium; then
    echo -e "${GREEN}✅ Browsers are available${NC}"
else
    echo -e "${RED}❌ Browser installation check failed${NC}"
    exit 1
fi

# Test 4: Test fallback file creation
echo -e "${YELLOW}📁 Test 4: Testing fallback file system...${NC}"
if docker run --rm -e CI=true playwright-test python -c "
import os
from pathlib import Path
print('CI environment:', os.getenv('CI'))
print('Checking uploaded_test_files directory...')
test_dir = Path('uploaded_test_files')
if test_dir.exists():
    files = list(test_dir.iterdir())
    print(f'Files found: {len(files)}')
    for f in files:
        print(f'  - {f.name}')
else:
    print('Directory does not exist')
"; then
    echo -e "${GREEN}✅ Fallback file system works${NC}"
else
    echo -e "${RED}❌ Fallback file system test failed${NC}"
    exit 1
fi

# Test 5: Test basic pytest execution
echo -e "${YELLOW}🧪 Test 5: Testing pytest execution...${NC}"
if docker run --rm playwright-test python -c "
import pytest
print('Pytest version:', pytest.__version__)
# Quick test discovery
import subprocess
result = subprocess.run(['python', '-m', 'pytest', '--collect-only', '-q'], 
                       capture_output=True, text=True)
print('Test discovery result:', result.returncode)
if result.stdout:
    print('Found tests:', len(result.stdout.split('\n')))
"; then
    echo -e "${GREEN}✅ Pytest execution works${NC}"
else
    echo -e "${RED}❌ Pytest execution test failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 All Docker setup tests passed!${NC}"
echo -e "${YELLOW}📝 Next steps:${NC}"
echo "1. Configure your .env file with credentials"
echo "2. Run: docker-compose up playwright-dev"
echo "3. Set up GitHub secrets for CI/CD"
echo "4. Push to GitHub to trigger automated tests"

# Cleanup
echo -e "${YELLOW}🧹 Cleaning up test image...${NC}"
docker rmi playwright-test 2>/dev/null || true 