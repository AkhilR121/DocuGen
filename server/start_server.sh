#!/bin/bash

echo "========================================"
echo "Starting DocuGen FastAPI Server"
echo "========================================"
echo ""

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo "ERROR: Poetry is not installed!"
    echo "Please install Poetry from: https://python-poetry.org/docs/#installation"
    echo ""
    echo "Mac/Linux installation:"
    echo "curl -sSL https://install.python-poetry.org | python3 -"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d ".venv" ] && [ ! -d "venv" ]; then
    echo "Installing dependencies..."
    poetry install
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies"
        exit 1
    fi
fi

# Environment selection (default: local)
ENV_NAME="${1:-local}"

echo ""
echo "Environment: $ENV_NAME"
echo "Starting server on http://localhost:8080"
echo "Docs available at http://localhost:8080/docs"
echo ""
echo "Press CTRL+C to stop the server"
echo "========================================"
echo ""

# Run the server
poetry run python run.py --env "$ENV_NAME"