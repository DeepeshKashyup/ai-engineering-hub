# MCP Tool for Gcloud Commands

## Overview
The MCP tool is designed to facilitate the execution of gcloud CLI commands in a programmatic way, enabling users to interact with Google Cloud Platform (GCP) services efficiently. It addresses the need for a streamlined approach to manage GCP resources, run SQL queries on BigQuery datasets, and handle large datasets/results.

## Features
- Execute gcloud CLI commands programmatically.
- Run SQL queries on Google BigQuery datasets.
- Download large datasets/results from BigQuery.
- Containerized environment for easy setup and deployment.
- Chart generation using Matplotlib to visualize data analysis results.
- Supports authentication and configuration management for GCP.
- Supports guarded execution of commands to ensure reliability.

## Tech Stack
- **Python**: The primary programming language for the tool.
- **MCP**: The Multi-Cloud Platform framework for executing gcloud commands.
- **gcloud**: The Google Cloud SDK for interacting with Google Cloud services.
- **BigQuery**: A serverless, highly scalable, and cost-effective multi-cloud data warehouse.
- **Docker**: For containerization and environment setup.
- **UV**: Fast Python package installer and resolver.

## Framework
- **FastMCP**: A framework for building multi-cloud applications, providing a structured way to manage cloud resources and execute commands.
- **google-cloud-sdk**: The official SDK for Google Cloud, used to interact with GCP services.
- **google-cloud-bigquery**: A client library for accessing BigQuery services.
- **Matplotlib**: A plotting library for creating static, animated, and interactive visualizations in Python.
- **Pandas**: A data manipulation and analysis library for Python.

## Folder Structure
```
gcp_mcp_server/
├── README.md
├── Dockerfile
├── pyproject.toml
├── uv.lock
├── server.py
├── controller/
│   ├── __init__.py
│   ├── schema_context.py
├── repository/
└── credentials/
    └── gcp-practitioner.json
```

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