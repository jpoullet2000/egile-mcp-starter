#!/bin/bash

# Development helper script for egile-mcp-starter
# Usage: ./scripts/dev.sh [command]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if poetry is installed
check_poetry() {
    if ! command -v poetry &> /dev/null; then
        print_error "Poetry is not installed. Please install it first."
        exit 1
    fi
}

# Install dependencies
install() {
    print_header "Installing dependencies"
    check_poetry
    poetry install
    print_success "Dependencies installed"
}

# Run tests
test() {
    print_header "Running tests"
    poetry run pytest tests/ -v --cov=egile_mcp_starter --cov-report=term-missing
    print_success "Tests completed"
}

# Run code quality checks
quality() {
    print_header "Running code quality checks"
    
    echo "Checking code formatting with Black..."
    poetry run black --check egile_mcp_starter tests || {
        print_warning "Code formatting issues found. Run 'poetry run black egile_mcp_starter tests' to fix."
    }
    
    echo "Checking import sorting with isort..."
    poetry run isort --check-only egile_mcp_starter tests || {
        print_warning "Import sorting issues found. Run 'poetry run isort egile_mcp_starter tests' to fix."
    }
    
    echo "Running flake8 linting..."
    poetry run flake8 egile_mcp_starter tests
    
    echo "Running mypy type checking..."
    poetry run mypy egile_mcp_starter
    
    print_success "Code quality checks completed"
}

# Format code
format() {
    print_header "Formatting code"
    poetry run black egile_mcp_starter tests
    poetry run isort egile_mcp_starter tests
    print_success "Code formatted"
}

# Test template generation
test_template() {
    print_header "Testing template generation"
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    echo "Using temporary directory: $TEMP_DIR"
    
    # Generate test project
    cd "$TEMP_DIR"
    cat > test-config.yaml << 'EOF'
default_context:
  project_name: "Test Server"
  project_slug: "test_server"
  project_description: "A test MCP server"
  author_name: "Test Author"
  author_email: "test@example.com"
  github_username: "testuser"
  version: "0.1.0"
  python_version: "3.11"
  use_docker: "y"
  use_github_actions: "y"
  use_pre_commit: "y"
  license: "MIT"
  include_examples: "y"
  server_type: "tools"
EOF
    
    # Go back to project root and generate
    cd - > /dev/null
    poetry run egile-mcp-starter --output-dir "$TEMP_DIR" --config-file "$TEMP_DIR/test-config.yaml" --no-input
    
    # Test the generated project
    cd "$TEMP_DIR/test_server"
    echo "Generated project structure:"
    ls -la
    
    # Test Poetry setup
    poetry install --no-interaction
    poetry run pytest --version
    
    print_success "Template generation test completed"
    echo "Generated project location: $TEMP_DIR/test_server"
}

# Build package
build() {
    print_header "Building package"
    rm -rf dist/
    poetry build
    print_success "Package built successfully"
    echo "Built files:"
    ls -la dist/
}

# Full development workflow
dev() {
    print_header "Running full development workflow"
    install
    format
    quality
    test
    test_template
    build
    print_success "Full development workflow completed successfully!"
}

# Clean up
clean() {
    print_header "Cleaning up"
    rm -rf dist/
    rm -rf .coverage
    rm -rf htmlcov/
    rm -rf .pytest_cache/
    rm -rf .mypy_cache/
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete
    print_success "Cleanup completed"
}

# Show help
help() {
    echo "Development helper script for egile-mcp-starter"
    echo ""
    echo "Usage:"
    echo "  ./scripts/dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  install        Install dependencies"
    echo "  test           Run tests with coverage"
    echo "  quality        Run code quality checks"
    echo "  format         Format code with Black and isort"
    echo "  test-template  Test template generation"
    echo "  build          Build the package"
    echo "  dev            Run full development workflow"
    echo "  clean          Clean up build artifacts"
    echo "  help           Show this help message"
    echo ""
}

# Main script logic
case "${1:-help}" in
    install)
        install
        ;;
    test)
        test
        ;;
    quality)
        quality
        ;;
    format)
        format
        ;;
    test-template)
        test_template
        ;;
    build)
        build
        ;;
    dev)
        dev
        ;;
    clean)
        clean
        ;;
    help|*)
        help
        ;;
esac
