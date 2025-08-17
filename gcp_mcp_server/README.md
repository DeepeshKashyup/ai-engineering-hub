# GCP MCP Server

## Overview
A Model Context Protocol (MCP) server that provides intelligent BigQuery integration with configurable knowledge base support. This tool enables AI agents to understand your database schema and execute SQL queries efficiently against Google BigQuery datasets.

## Features
- **BigQuery Integration**: Execute SQL queries programmatically against BigQuery datasets
- **Intelligent Schema Context**: AI-powered understanding of your database structure
- **Flexible Knowledge Base**: Support for both local files and Google Cloud Storage buckets
- **Secure Credential Handling**: Volume-mounted credentials with no embedded secrets
- **Containerized Deployment**: Docker support for easy setup and deployment
- **MCP Protocol Compliance**: Standard Model Context Protocol implementation
- **Health Monitoring**: Built-in health check endpoints

## Knowledge Base Features
- **Local Knowledge Base**: Store schema and sample queries in local JSON files
- **GCS Integration**: Read knowledge base from Google Cloud Storage buckets
- **Schema Documentation**: Detailed table schemas with relationships and descriptions
- **Query Examples**: Sample queries to guide AI query generation
- **Automatic Fallbacks**: Default schema if knowledge base files are unavailable

## Tech Stack
- **Python 3.11**: Primary programming language with async support
- **FastMCP**: Framework for building Model Context Protocol servers
- **Google Cloud BigQuery**: Serverless data warehouse integration
- **Google Cloud Storage**: Knowledge base file storage (optional)
- **Docker**: Containerization for consistent deployment
- **UV**: Fast Python package installer and resolver

## Framework Components
- **FastMCP v2.11.3**: MCP server framework with HTTP transport
- **google-cloud-bigquery**: Official BigQuery client library
- **google-cloud-storage**: GCS client for knowledge base files
- **Python Typing**: Full type hints for better code quality
- **Pathlib**: Modern path handling for cross-platform compatibility

## Folder Structure
```
gcp_mcp_server/
├── README.md
├── Dockerfile
├── Dockerfile.public
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── server.py
├── controller/
│   └── schema_context.py
├── knowledge_base/
│   ├── schema.json
│   └── sample_queries.json
├── credentials/
│   └── gcp-practitioner.json
├── run-server.sh
├── run-server.ps1
├── QUICK_START.md
└── DOCKER_USAGE.md
```

## Knowledge Base Configuration

### Local Knowledge Base (Default)
Place your schema and query files in the `knowledge_base/` directory:

**schema.json** - Define your database schema:
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

**sample_queries.json** - Provide example queries:
```json
{
  "user_analytics": [
    "SELECT COUNT(*) FROM users WHERE signup_date >= '2024-01-01'",
    "SELECT country, COUNT(*) as user_count FROM users GROUP BY country"
  ]
}
```

### GCS Bucket Knowledge Base
Set the `KNOWLEDGE_BASE_BUCKET` environment variable:
```bash
export KNOWLEDGE_BASE_BUCKET=gs://your-bucket/path/to/knowledge-base
```

The server will automatically read `schema.json` and `sample_queries.json` from the specified GCS location.

## Usage

### Running with Python

To start the server locally, run the following command:

```bash
python server.py
```

### Running with Docker

1. First, build the Docker image:
```bash
docker build -t gcp-mcp-server .
```

2. Run the container with your GCP credentials:
```bash
docker run -d \
  -p 8001:8001 \
  -v /path/to/your/credentials.json:/app/credentials/gcp-practitioner.json:ro \
  -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcp-practitioner.json \
  --name gcp-mcp-server \
  gcp-mcp-server
```

Replace `/path/to/your/credentials.json` with the actual path to your GCP credentials file.

### Environment Variables

- `PORT`: The port on which the server will run (default: 8001)
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to your GCP credentials file

### Authentication

1. Place your GCP credentials JSON file in the `credentials/` directory as `gcp-practitioner.json`
2. The server will automatically use these credentials for authentication

## Testing the Server

Once the server is running, you can test it using:

```bash
curl http://localhost:8001/mcp/health_check
```

You should receive a response indicating the server is healthy.

## Security Notes

- Never commit your GCP credentials file to version control
- Always use volume mounting for credentials when running with Docker
- Keep your credentials file in a secure location
- Use appropriate file permissions for your credentials file