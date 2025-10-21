#!/bin/bash

# Synthetic Financial Dataset Generator - Project Setup Script
# This script sets up the complete project structure and dependencies

echo "🏦 Synthetic Financial Dataset Generator - Setup Script"
echo "========================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    print_error "Conda is not installed. Please install Miniconda or Anaconda first."
    echo "Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

print_status "Conda found"

# Create project structure
print_status "Creating project structure..."

mkdir -p src/config
mkdir -p src/generators
mkdir -p src/validators
mkdir -p src/utils
mkdir -p src/llm
mkdir -p tests
mkdir -p data/output
mkdir -p data/templates
mkdir -p logs

# Create __init__.py files
touch src/__init__.py
touch src/config/__init__.py
touch src/generators/__init__.py
touch src/validators/__init__.py
touch src/utils/__init__.py
touch src/llm/__init__.py
touch tests/__init__.py

# Create .gitkeep for empty directories
touch data/output/.gitkeep
touch data/templates/.gitkeep

print_status "Project structure created"

# Create conda environment
print_status "Creating conda environment 'findata-gen'..."

if conda env list | grep -q "findata-gen"; then
    print_warning "Environment 'findata-gen' already exists. Skipping creation."
else
    conda env create -f environment.yml
    if [ $? -eq 0 ]; then
        print_status "Conda environment created successfully"
    else
        print_error "Failed to create conda environment"
        exit 1
    fi
fi

# Activate environment and install package
print_status "Activating environment and installing package..."

# Source conda.sh to enable conda activate in script
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate findata-gen

if [ $? -eq 0 ]; then
    print_status "Environment activated"
else
    print_error "Failed to activate environment"
    exit 1
fi

# Install package in development mode
pip install -e .
print_status "Package installed in development mode"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file and add your API keys:"
    echo "  - GEMINI_API_KEY (required)"
    echo "  - GOOGLE_SEARCH_API_KEY (optional)"
    echo ""
    echo "Get your Gemini API key from: https://makersuite.google.com/app/apikey"
else
    print_warning ".env file already exists. Skipping."
fi

# Run tests
print_status "Running tests..."
pytest tests/ -v

if [ $? -eq 0 ]; then
    print_status "All tests passed"
else
    print_warning "Some tests failed. This might be due to missing API keys."
fi

# Print success message
echo ""
echo "========================================================"
echo -e "${GREEN}✨ Setup Complete!${NC}"
echo "========================================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env file and add your GEMINI_API_KEY"
echo "  2. Activate the environment: conda activate findata-gen"
echo "  3. Run the application: python src/app.py"
echo "  4. Open browser at: http://localhost:7860"
echo ""
echo "For more information, see:"
echo "  - README.md for full documentation"
echo "  - QUICKSTART.md for quick start guide"
echo ""
echo "Happy data generating! 🚀"