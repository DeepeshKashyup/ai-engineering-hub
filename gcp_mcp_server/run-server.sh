#!/bin/bash

# GCP MCP Server Docker Runner Script
# This script makes it easy to run the GCP MCP Server with your credentials

set -e

# Default values
CONTAINER_NAME="gcp-mcp-server"
IMAGE_NAME="gcp-mcp-server"
PORT="8000"
CREDENTIALS_FILE=""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    -c, --credentials FILE    Path to GCP credentials JSON file (required)
    -n, --name NAME          Container name (default: gcp-mcp-server)
    -p, --port PORT          Port to expose (default: 8000)
    -i, --image IMAGE        Docker image name (default: gcp-mcp-server)
    -h, --help               Show this help message

Examples:
    $0 -c /path/to/gcp-credentials.json
    $0 --credentials ./my-creds.json --port 8080 --name my-server
    $0 -c gcp-key.json -n prod-server -p 9000

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--credentials)
            CREDENTIALS_FILE="$2"
            shift 2
            ;;
        -n|--name)
            CONTAINER_NAME="$2"
            shift 2
            ;;
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -i|--image)
            IMAGE_NAME="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [[ -z "$CREDENTIALS_FILE" ]]; then
    print_error "Credentials file is required. Use -c or --credentials option."
    show_usage
    exit 1
fi

# Check if credentials file exists
if [[ ! -f "$CREDENTIALS_FILE" ]]; then
    print_error "Credentials file not found: $CREDENTIALS_FILE"
    exit 1
fi

# Get absolute path of credentials file
CREDENTIALS_FILE=$(realpath "$CREDENTIALS_FILE")

print_info "Starting GCP MCP Server..."
print_info "Container name: $CONTAINER_NAME"
print_info "Port: $PORT"
print_info "Credentials: $CREDENTIALS_FILE"
print_info "Image: $IMAGE_NAME"

# Stop existing container if it exists
if docker ps -a --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    print_warning "Stopping existing container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
    docker rm "$CONTAINER_NAME" >/dev/null 2>&1 || true
fi

# Run the container
print_info "Starting new container..."
docker run -d \
    --name "$CONTAINER_NAME" \
    -p "$PORT:8000" \
    -v "$CREDENTIALS_FILE:/app/credentials/gcp-credentials.json:ro" \
    -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcp-credentials.json \
    "$IMAGE_NAME"

# Wait a moment for the container to start
sleep 3

# Check if container is running
if docker ps --format 'table {{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
    print_info "✅ Container started successfully!"
    print_info "🌐 Server URL: http://localhost:$PORT/mcp"
    print_info "📋 Container name: $CONTAINER_NAME"
    
    echo ""
    print_info "Useful commands:"
    echo "  View logs:    docker logs $CONTAINER_NAME"
    echo "  Stop server:  docker stop $CONTAINER_NAME"
    echo "  Remove:       docker rm $CONTAINER_NAME"
    echo "  Test server:  curl http://localhost:$PORT/mcp"
else
    print_error "Failed to start container. Check Docker logs:"
    docker logs "$CONTAINER_NAME" 2>/dev/null || true
    exit 1
fi
