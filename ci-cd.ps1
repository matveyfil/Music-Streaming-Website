# Stop execution if any command fails
$ErrorActionPreference = "Stop"

# Pull the latest images from Docker Hub (if necessary)
Write-Host "Pulling the latest images from Docker Hub..."
docker-compose pull

# Build the Docker image
Write-Host "Building Docker image..."
docker-compose build

# Run tests
Write-Host "Running tests..."
docker-compose run --rm catalog python -m pytest /app/tests/

Write-Host "CI/CD process completed successfully!"
