# Quick Start Guide

## 🚀 How to Use the GCP MCP Server Docker Image

This Docker image allows anyone to run a GCP MCP (Model Context Protocol) server with their own credentials.

### Prerequisites
- Docker installed on your system
- A GCP service account key file (JSON format)

### Option 1: Simple Run (Recommended)

```bash
# Download your GCP service account key and save it as 'gcp-credentials.json'
# Then run:
docker run -d \
  -p 8000:8000 \
  -v ./gcp-credentials.json:/app/credentials/gcp-credentials.json:ro \
  --name my-gcp-mcp-server \
  gcp-mcp-server:public
```

### Option 2: Using the Helper Scripts

#### On Linux/Mac:
```bash
# Make the script executable
chmod +x run-server.sh

# Run with your credentials
./run-server.sh -c /path/to/your-gcp-credentials.json
```

#### On Windows:
```powershell
# Run with your credentials
.\run-server.ps1 -CredentialsFile "C:\path\to\your-gcp-credentials.json"
```

### Option 3: Using Docker Compose

1. **Create a `docker-compose.yml` file:**
   ```yaml
   version: '3.8'
   services:
     gcp-mcp-server:
       image: gcp-mcp-server:public
       container_name: my-gcp-mcp-server
       ports:
         - "8000:8000"
       volumes:
         - ./gcp-credentials.json:/app/credentials/gcp-credentials.json:ro
       restart: unless-stopped
   ```

2. **Run the service:**
   ```bash
   docker-compose up -d
   ```

### Testing Your Server

Once running, test your server:

```bash
# Check if it's responding
curl http://localhost:8000/mcp

# View logs
docker logs my-gcp-mcp-server

# Stop the server
docker stop my-gcp-mcp-server
```

### Environment Variables

You can customize the server using these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Server port | `8000` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to credentials | `/app/credentials/gcp-credentials.json` |

### Example with Custom Port

```bash
docker run -d \
  -p 9000:9000 \
  -e PORT=9000 \
  -v ./gcp-credentials.json:/app/credentials/gcp-credentials.json:ro \
  --name my-gcp-mcp-server \
  gcp-mcp-server:public
```

### Security Best Practices

✅ **DO:**
- Use read-only volume mounts (`:ro`)
- Keep your credentials file secure
- Use specific container names
- Limit port exposure

❌ **DON'T:**
- Include credentials in the Docker image
- Use world-readable credential files
- Expose unnecessary ports
- Run containers as root (handled automatically)

### Troubleshooting

**Container won't start?**
- Check that your credentials file exists and is readable
- Verify the file path in the volume mount
- Check Docker logs: `docker logs my-gcp-mcp-server`

**Can't connect to the server?**
- Ensure the port is properly mapped
- Check if another service is using port 8000
- Verify the container is running: `docker ps`

**BigQuery permission errors?**
- Verify your service account has BigQuery access
- Check that the credentials file is valid JSON
- Ensure the project ID is correct in your GCP console
