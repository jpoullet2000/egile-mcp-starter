#!/bin/bash

# Release helper script for egile-mcp-starter
# Usage: ./scripts/release.sh [version]

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

# Check if we're on main branch
check_branch() {
    local current_branch=$(git branch --show-current)
    if [ "$current_branch" != "main" ]; then
        print_error "You must be on the main branch to create a release. Current branch: $current_branch"
        exit 1
    fi
}

# Check if working directory is clean
check_clean() {
    if [ -n "$(git status --porcelain)" ]; then
        print_error "Working directory is not clean. Please commit or stash your changes."
        git status --short
        exit 1
    fi
}

# Check if version is provided
check_version() {
    if [ -z "$1" ]; then
        print_error "Version number is required"
        echo "Usage: ./scripts/release.sh [version]"
        echo "Example: ./scripts/release.sh 1.0.0"
        exit 1
    fi
}

# Validate version format
validate_version() {
    local version=$1
    if ! [[ $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        print_error "Invalid version format. Use semantic versioning (e.g., 1.0.0)"
        exit 1
    fi
}

# Get current version from pyproject.toml
get_current_version() {
    grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/'
}

# Update version in pyproject.toml
update_version() {
    local new_version=$1
    local current_version=$(get_current_version)
    
    print_header "Updating version from $current_version to $new_version"
    
    # Update pyproject.toml
    sed -i "s/^version = \".*\"/version = \"$new_version\"/" pyproject.toml
    
    # Update template's pyproject.toml if it has a hardcoded version
    if [ -f "{{cookiecutter.project_slug}}/pyproject.toml" ]; then
        sed -i "s/version = \"{{cookiecutter.version}}\"/version = \"{{cookiecutter.version}}\"/" "{{cookiecutter.project_slug}}/pyproject.toml"
    fi
    
    print_success "Version updated to $new_version"
}

# Run full test suite
run_tests() {
    print_header "Running full test suite"
    ./scripts/dev.sh dev
    print_success "All tests passed"
}

# Create git tag and push
create_release() {
    local version=$1
    
    print_header "Creating release $version"
    
    # Add and commit version changes
    git add pyproject.toml
    git commit -m "bump: version $version"
    
    # Create annotated tag
    git tag -a "v$version" -m "Release version $version"
    
    # Push changes and tag
    git push origin main
    git push origin "v$version"
    
    print_success "Release $version created and pushed"
    echo ""
    echo "Next steps:"
    echo "1. Go to GitHub and create a release from the tag v$version"
    echo "2. The CI/CD pipeline will automatically publish to PyPI"
    echo "3. Docker images will be built and published"
}

# Show release information
show_info() {
    local version=$1
    local current_version=$(get_current_version)
    
    echo "Release Information:"
    echo "==================="
    echo "Current version: $current_version"
    echo "New version: $version"
    echo "Branch: $(git branch --show-current)"
    echo "Last commit: $(git log -1 --format='%h - %s (%an, %ar)')"
    echo ""
}

# Rollback if something goes wrong
rollback() {
    local version=$1
    print_warning "Rolling back changes..."
    
    # Reset any uncommitted changes
    git checkout -- pyproject.toml
    
    # Remove tag if it was created
    if git tag -l | grep -q "v$version"; then
        git tag -d "v$version"
        print_warning "Removed local tag v$version"
    fi
}

# Main release function
release() {
    local version=$1
    
    # Trap errors and rollback
    trap 'rollback $version' ERR
    
    # Pre-flight checks
    check_version "$version"
    validate_version "$version"
    check_branch
    check_clean
    
    # Show information
    show_info "$version"
    
    # Confirm with user
    echo -n "Proceed with release? [y/N]: "
    read -r confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        print_warning "Release cancelled"
        exit 0
    fi
    
    # Run the release process
    update_version "$version"
    run_tests
    create_release "$version"
    
    print_success "Release $version completed successfully!"
}

# Show help
help() {
    echo "Release helper script for egile-mcp-starter"
    echo ""
    echo "Usage:"
    echo "  ./scripts/release.sh [version]"
    echo ""
    echo "Example:"
    echo "  ./scripts/release.sh 1.0.0"
    echo ""
    echo "This script will:"
    echo "  1. Check that you're on the main branch with a clean working directory"
    echo "  2. Update the version in pyproject.toml"
    echo "  3. Run the full test suite"
    echo "  4. Create a git commit and tag"
    echo "  5. Push to GitHub"
    echo ""
    echo "After running this script:"
    echo "  - Create a GitHub release from the new tag"
    echo "  - The CI/CD pipeline will automatically publish to PyPI"
    echo ""
}

# Main script logic
if [ $# -eq 0 ]; then
    help
    exit 1
fi

case "$1" in
    -h|--help|help)
        help
        ;;
    *)
        release "$1"
        ;;
esac
