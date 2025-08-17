# GCP MCP Server Docker Image

A Docker image for running a Model Context Protocol (MCP) server that provides BigQuery integration with configurable knowledge base support.

## Features

- **BigQuery Integration**: Execute SQL queries against Google BigQuery
- **Schema Context**: Intelligent schema understanding for better query generation
- **Knowledge Base Support**: 
  - Local knowledge base files (default)
  - Google Cloud Storage bucket integration
- **Secure Credential Handling**: Volume-mounted credentials (no embedded secrets)

## Quick Start

### Option 1: Using Volume Mount with Local Knowledge Base (Recommended)

1. **Prepare your GCP credentials file**:
   - Download your GCP service account key as JSON
   - Save it as `gcp-credentials.json`

2. **Run the container**:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v /path/to/your/gcp-credentials.json:/app/credentials/gcp-credentials.json:ro \
     --name my-gcp-mcp-server \
     gcp-mcp-server
   ```

### Option 2: Using GCS Bucket for Knowledge Base

1. **Set up with GCS bucket**:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v /path/to/your/gcp-credentials.json:/app/credentials/gcp-credentials.json:ro \
     -e KNOWLEDGE_BASE_BUCKET=gs://your-bucket-name/path/to/knowledge-base \
     --name my-gcp-mcp-server \
     gcp-mcp-server
   ```

### Option 3: Using Environment Variables

1. **Set the credentials path**:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -v /path/to/your/credentials-directory:/app/credentials:ro \
     -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/your-file.json \
     --name my-gcp-mcp-server \
     gcp-mcp-server
   ```

### Option 3: Using Docker Compose

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  gcp-mcp-server:
    image: gcp-mcp-server
    container_name: my-gcp-mcp-server
    ports:
      - "8000:8000"
    volumes:
      - ./gcp-credentials.json:/app/credentials/gcp-credentials.json:ro
    environment:
      - PORT=8000
      - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcp-credentials.json
    restart: unless-stopped
```

Then run:
```bash
docker-compose up -d
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP credentials | `/app/credentials/gcp-credentials.json` |
| `KNOWLEDGE_BASE_BUCKET` | GCS bucket path for knowledge base (optional) | Not set (uses local files) |

## Knowledge Base Configuration

The server supports two modes for knowledge base management:

### Local Knowledge Base (Default)
The server looks for knowledge base files in the `knowledge_base/` directory:
- `schema.json` - Database schema definitions
- `sample_queries.json` - Example queries for AI guidance

### GCS Bucket Knowledge Base
Set the `KNOWLEDGE_BASE_BUCKET` environment variable to use a GCS bucket:
```bash
# Format: gs://bucket-name/path/to/knowledge-base
KNOWLEDGE_BASE_BUCKET=gs://my-company-kb/bigquery-schemas

# Or just the bucket name if files are in the root
KNOWLEDGE_BASE_BUCKET=gs://my-knowledge-base
```

The server will look for the same JSON files in the specified GCS location.

### Knowledge Base File Formats

**schema.json example:**
```json
{
  "users": {
    "columns": ["id", "name", "email", "signup_date"],
    "relationships": {
      "orders": {"local_key": "id", "foreign_key": "user_id"}
    },
    "description": "User account information"
  }
}
```

**sample_queries.json example:**
```json
{
  "user_analytics": [
    "SELECT COUNT(*) FROM users WHERE signup_date >= '2024-01-01'",
    "SELECT country, COUNT(*) as user_count FROM users GROUP BY country"
  ]
}
```

## Available Endpoints

- **Health Check**: `GET http://localhost:8000/mcp`
- **MCP Protocol**: `POST http://localhost:8000/mcp`

## Available MCP Tools

1. **`health_check`** - Server health monitoring
2. **`schema_context`** - Get BigQuery table schemas
3. **`query_bigquery`** - Execute BigQuery SQL queries

## Building the Image

To build the image yourself:

```bash
# Clone the repository
git clone <repository-url>
cd gcp_mcp_server

# Build the image
docker build -f Dockerfile.public -t gcp-mcp-server .

# Or build with a specific tag
docker build -f Dockerfile.public -t your-username/gcp-mcp-server:latest .
```

## Publishing to Docker Hub

```bash
# Build and tag for Docker Hub
docker build -f Dockerfile.public -t your-username/gcp-mcp-server:latest .

# Push to Docker Hub
docker push your-username/gcp-mcp-server:latest
```

## Security Notes

- **Never include credentials in the Docker image**
- **Always use volume mounts or environment variables for sensitive data**
- **Use read-only volume mounts when possible**
- **Keep your GCP credentials file secure and with minimal permissions**

## Troubleshooting

### Common Issues

1. **"No credentials found"**:
   - Ensure your credentials file is properly mounted
   - Check the `GOOGLE_APPLICATION_CREDENTIALS` environment variable
   - Verify file permissions (should be readable by user 1000)

2. **"Connection refused"**:
   - Check if the container is running: `docker ps`
   - Verify port mapping: `-p 8000:8000`
   - Check container logs: `docker logs my-gcp-mcp-server`

3. **"Permission denied"**:
   - Ensure the credentials file has proper permissions
   - Use read-only mounts: `:ro`

### Checking Logs

```bash
# View container logs
docker logs my-gcp-mcp-server

# Follow logs in real-time
docker logs -f my-gcp-mcp-server
```

### Testing the Server

```bash
# Test health endpoint
curl http://localhost:8000/mcp

# Check if container is responding
docker exec my-gcp-mcp-server curl -f http://localhost:8000/mcp
```
