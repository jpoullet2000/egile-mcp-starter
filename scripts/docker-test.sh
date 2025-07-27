#!/bin/bash

# Docker build test script for egile-mcp-starter
# Usage: ./scripts/docker-test.sh

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🐳 Testing Docker build for egile-mcp-starter...${NC}"

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not available in this environment${NC}"
    echo -e "${YELLOW}ℹ️  This script requires Docker to be installed and running${NC}"
    exit 1
fi

# Build the Docker image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
docker build -t egile-mcp-starter:test .

# Test the image
echo -e "${YELLOW}🧪 Testing the built image...${NC}"
docker run --rm egile-mcp-starter:test --help

# Test with volume mount
echo -e "${YELLOW}📁 Testing with volume mount...${NC}"
mkdir -p ./test-docker-output
docker run --rm \
    -v "$(pwd)/test-docker-output:/app/output" \
    egile-mcp-starter:test \
    --output-dir /app/output \
    --no-input

# Check if files were created
if [ -d "./test-docker-output" ] && [ "$(ls -A ./test-docker-output)" ]; then
    echo -e "${GREEN}✅ Docker build and execution successful!${NC}"
    echo -e "${GREEN}✅ Files created in test-docker-output/${NC}"
    ls -la ./test-docker-output/
else
    echo -e "${RED}❌ Docker test failed - no output files created${NC}"
    exit 1
fi

# Cleanup
echo -e "${YELLOW}🧹 Cleaning up test files...${NC}"
rm -rf ./test-docker-output

echo -e "${GREEN}🎉 Docker test completed successfully!${NC}"
