# GCP MCP Server Docker Runner PowerShell Script
# This script makes it easy to run the GCP MCP Server with your credentials on Windows

param(
    [Parameter(Mandatory=$true, HelpMessage="Path to GCP credentials JSON file")]
    [string]$CredentialsFile,
    
    [Parameter(HelpMessage="Container name")]
    [string]$ContainerName = "gcp-mcp-server",
    
    [Parameter(HelpMessage="Port to expose")]
    [int]$Port = 8000,
    
    [Parameter(HelpMessage="Docker image name")]
    [string]$ImageName = "gcp-mcp-server",
    
    [Parameter(HelpMessage="Show help message")]
    [switch]$Help
)

# Function to write colored output
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Show help if requested
if ($Help) {
    Write-Host @"
GCP MCP Server Docker Runner

USAGE:
    .\run-server.ps1 -CredentialsFile <path> [OPTIONS]

PARAMETERS:
    -CredentialsFile    Path to GCP credentials JSON file (required)
    -ContainerName      Container name (default: gcp-mcp-server)
    -Port              Port to expose (default: 8000)
    -ImageName         Docker image name (default: gcp-mcp-server)
    -Help              Show this help message

EXAMPLES:
    .\run-server.ps1 -CredentialsFile "C:\path\to\gcp-credentials.json"
    .\run-server.ps1 -CredentialsFile ".\my-creds.json" -Port 8080 -ContainerName "my-server"

"@
    exit 0
}

# Validate credentials file
if (-not (Test-Path $CredentialsFile)) {
    Write-Error "Credentials file not found: $CredentialsFile"
    exit 1
}

# Get absolute path of credentials file
$CredentialsFile = Resolve-Path $CredentialsFile

Write-Info "Starting GCP MCP Server..."
Write-Info "Container name: $ContainerName"
Write-Info "Port: $Port"
Write-Info "Credentials: $CredentialsFile"
Write-Info "Image: $ImageName"

# Stop existing container if it exists
try {
    $existingContainer = docker ps -a --format "table {{.Names}}" | Where-Object { $_ -eq $ContainerName }
    if ($existingContainer) {
        Write-Warning "Stopping existing container: $ContainerName"
        docker stop $ContainerName 2>$null | Out-Null
        docker rm $ContainerName 2>$null | Out-Null
    }
} catch {
    # Ignore errors if container doesn't exist
}

# Run the container
Write-Info "Starting new container..."
try {
    $containerId = docker run -d `
        --name $ContainerName `
        -p "${Port}:8000" `
        -v "${CredentialsFile}:/app/credentials/gcp-credentials.json:ro" `
        -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcp-credentials.json `
        $ImageName

    # Wait a moment for the container to start
    Start-Sleep -Seconds 3

    # Check if container is running
    $runningContainer = docker ps --format "table {{.Names}}" | Where-Object { $_ -eq $ContainerName }
    
    if ($runningContainer) {
        Write-Info "✅ Container started successfully!"
        Write-Info "🌐 Server URL: http://localhost:$Port/mcp"
        Write-Info "📋 Container name: $ContainerName"
        
        Write-Host ""
        Write-Info "Useful commands:"
        Write-Host "  View logs:    docker logs $ContainerName"
        Write-Host "  Stop server:  docker stop $ContainerName"
        Write-Host "  Remove:       docker rm $ContainerName"
        Write-Host "  Test server:  Invoke-WebRequest http://localhost:$Port/mcp"
    } else {
        Write-Error "Failed to start container. Check Docker logs:"
        docker logs $ContainerName 2>$null
        exit 1
    }
} catch {
    Write-Error "Failed to start container: $_"
    exit 1
}
