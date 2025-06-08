#!/bin/bash

# Ensure script stops on first error
set -e

# Check if version type is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <major|minor|patch>"
    exit 1
fi

VERSION_TYPE=$1

# Validate version type
if [[ ! $VERSION_TYPE =~ ^(major|minor|patch)$ ]]; then
    echo "Error: Version type must be 'major', 'minor', or 'patch'"
    exit 1
fi

echo "Starting release process..."

# Ensure we're on the master branch
git checkout master
git pull

# Run tests
echo "Running tests..."
pytest

# Run type checking
echo "Running type checking..."
mypy STanalysis

# Update version
echo "Bumping $VERSION_TYPE version..."
bumpver update --$VERSION_TYPE

# Build package
echo "Building package..."
python -m build

# Upload to PyPI
echo "Uploading to PyPI..."
twine upload -u $TWINE_USERNAME -p $TWINE_PASSWORD dist/*

echo "Release process completed successfully!"
