param(
    [string]$ImageName,        # Name of the Docker image to build
    [string]$Tag,              # Tag for the Docker image
    [string]$DockerfilePath = "."  # Path to the Dockerfile, defaults to the current directory
)

try {
    # Attempt to build the Docker image using the provided Dockerfile
    Write-Host "Building Docker image ${ImageName}:${Tag}..."
    docker build -t "${ImageName}:${Tag}" -f $DockerfilePath .
    if ($LASTEXITCODE -ne 0) {  # Check if the build command was successful
        Write-Host "Docker build failed."
        exit 1  # Exit the script with an error code if the build failed
    }
    Write-Host "Docker image built successfully."

    # Attempt to push the built image to a Docker registry
    Write-Host "Pushing Docker image ${ImageName}:${Tag}..."
    docker push "${ImageName}:${Tag}"
    if ($LASTEXITCODE -ne 0) {  # Check if the push command was successful
        Write-Host "Failed to push the Docker image."
        exit 1  # Exit the script with an error code if the push failed
    }
    Write-Host "Image ${ImageName}:${Tag} has been built and pushed successfully to the Docker registry."
}
catch {
    # Handle any exceptions that occur during the build or push process
    Write-Host "An error occurred: $($_.Exception.Message)"
}


#.\scriptname.ps1 -ImageName "yourimagename" -Tag "yourtag"