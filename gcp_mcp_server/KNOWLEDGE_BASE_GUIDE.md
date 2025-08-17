# Knowledge Base Configuration Guide

## Overview

The GCP MCP Server supports flexible knowledge base configuration to help AI agents understand your database schema and generate better queries. You can use either local files or Google Cloud Storage buckets to store your knowledge base.

## Features

- **Local Knowledge Base**: Store schema and sample queries in local JSON files
- **GCS Integration**: Read knowledge base from Google Cloud Storage buckets
- **Automatic Fallback**: Uses default schema if knowledge base files are unavailable
- **Rich Schema Support**: Detailed table descriptions, relationships, and sample queries

## Configuration Methods

### Method 1: Local Knowledge Base (Default)

Place your knowledge base files in the `knowledge_base/` directory:

```
knowledge_base/
├── schema.json
└── sample_queries.json
```

### Method 2: GCS Bucket Knowledge Base

Set the `KNOWLEDGE_BASE_BUCKET` environment variable:

```bash
export KNOWLEDGE_BASE_BUCKET=gs://your-bucket-name/path/to/knowledge-base
```

The server will look for the same JSON files in the specified GCS location.

## File Formats

### schema.json

Defines your database structure with tables, columns, relationships, and descriptions:

```json
{
  "users": {
    "columns": ["id", "name", "email", "signup_date", "country"],
    "relationships": {
      "orders": {"local_key": "id", "foreign_key": "user_id"},
      "user_sessions": {"local_key": "id", "foreign_key": "user_id"}
    },
    "description": "User account information and registration details"
  },
  "orders": {
    "columns": ["order_id", "user_id", "amount", "created_at", "status"],
    "relationships": {
      "users": {"local_key": "user_id", "foreign_key": "id"}
    },
    "description": "Customer order transactions and purchase history"
  }
}
```

### sample_queries.json

Provides example queries organized by category to guide AI query generation:

```json
{
  "user_analytics": [
    "SELECT u.country, COUNT(*) as user_count FROM users u GROUP BY u.country ORDER BY user_count DESC",
    "SELECT DATE(u.signup_date) as signup_day, COUNT(*) as new_users FROM users u GROUP BY DATE(u.signup_date) ORDER BY signup_day DESC LIMIT 30"
  ],
  "sales_analysis": [
    "SELECT u.name, SUM(o.amount) as total_spent FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.id, u.name ORDER BY total_spent DESC LIMIT 10"
  ]
}
```

## Docker Usage

### Local Knowledge Base with Docker

```bash
docker run -d \
  -p 8000:8000 \
  -v /path/to/your/gcp-credentials.json:/app/credentials/gcp-credentials.json:ro \
  -v /path/to/your/knowledge_base:/app/knowledge_base:ro \
  --name my-gcp-mcp-server \
  gcp-mcp-server
```

### GCS Knowledge Base with Docker

```bash
docker run -d \
  -p 8000:8000 \
  -v /path/to/your/gcp-credentials.json:/app/credentials/gcp-credentials.json:ro \
  -e KNOWLEDGE_BASE_BUCKET=gs://your-bucket-name/knowledge-base \
  --name my-gcp-mcp-server \
  gcp-mcp-server
```

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `KNOWLEDGE_BASE_BUCKET` | GCS bucket path for knowledge base | `gs://my-company-kb/bigquery-schemas` |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to GCP credentials | `/app/credentials/gcp-credentials.json` |

## Best Practices

1. **Schema Organization**: Group related tables together in your schema
2. **Relationship Mapping**: Always define foreign key relationships for better JOIN generation
3. **Query Examples**: Provide diverse sample queries covering common use cases
4. **Descriptions**: Add meaningful descriptions for complex tables
5. **Version Control**: Keep your knowledge base files in version control
6. **GCS Security**: Use IAM roles to control access to GCS knowledge base buckets

## Troubleshooting

### Common Issues

1. **Knowledge base files not found**: Check file paths and permissions
2. **GCS access denied**: Verify IAM permissions for the service account
3. **Invalid JSON format**: Validate JSON syntax in your files
4. **Missing relationships**: Ensure all foreign keys are properly defined

### Debug Output

The server logs will show which knowledge base method is being used:
- `"Using local knowledge base directory"` - Loading from local files
- `"Loading knowledge base from GCS bucket: <bucket-path>"` - Loading from GCS

### Testing

Use the included test script to verify your knowledge base configuration:

```bash
uv run python test_knowledge_base.py
```

This will show the parsed schema and sample queries, helping you verify the configuration.
