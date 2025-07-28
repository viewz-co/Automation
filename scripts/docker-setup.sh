#!/bin/bash

# Docker Setup Script for Playwright Framework
# This script sets up the containerized testing environment

set -e

echo "🐳 Setting up Docker environment for Playwright tests..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker and Docker Compose are installed${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️ .env file not found. Creating from template...${NC}"
    
    if [ -f env_template.txt ]; then
        cp env_template.txt .env
        echo -e "${BLUE}📝 Please edit .env file with your credentials:${NC}"
        echo "  - TEST_USERNAME"
        echo "  - TEST_PASSWORD" 
        echo "  - TEST_TOTP_SECRET"
        echo "  - TESTRAIL_URL"
        echo "  - TESTRAIL_USERNAME"
        echo "  - TESTRAIL_PASSWORD"
        echo "  - TESTRAIL_PROJECT_ID"
    else
        echo -e "${RED}❌ env_template.txt not found. Please create .env file manually.${NC}"
        exit 1
    fi
fi

# Create necessary directories
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p reports screenshots uploaded_test_files

# Build Docker images
echo -e "${BLUE}🔨 Building Docker images...${NC}"
docker-compose build

echo -e "${GREEN}✅ Docker environment setup complete!${NC}"
echo ""
echo -e "${BLUE}🚀 Available commands:${NC}"
echo "  docker-compose up playwright-dev      # Run development tests"
echo "  docker-compose up playwright-test     # Run production tests"
echo "  docker-compose up upload-tests        # Run upload tests only"
echo "  docker-compose up parallel-tests      # Run tests in parallel"
echo ""
echo -e "${BLUE}📊 View reports:${NC}"
echo "  reports/report.html                   # Test report"
echo "  screenshots/                          # Failure screenshots"
echo ""
echo -e "${YELLOW}⚠️ Don't forget to configure your .env file with actual credentials!${NC}" 