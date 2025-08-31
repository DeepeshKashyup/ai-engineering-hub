# MCP Client Usage Guide

This `client/` directory contains lean, reusable clients for your BigQuery MCP server.

## Files in client/

### 📄 `MCPClient.py`
**Async MCP Client** - Main client class for async applications
- Full-featured async client
- Context manager support
- Error handling
- Convenience methods for all tools

### 📄 `SyncMCPClient.py` 
**Sync MCP Client** - Synchronous wrapper for non-async code
- Synchronous wrapper around MCPClient
- Works in regular Python scripts
- No async/await needed

### 📄 `demo_client.py`
**Usage Examples** - Comprehensive demo showing all features
- Basic usage patterns
- Error handling examples
- Custom query demonstrations

### 📄 `test_client.py`
**Test Suite** - Complete test suite for the MCP server
- Health checks
- Schema validation
- Query testing

### 📄 `__init__.py`
**Package Init** - Makes client/ a proper Python package
- Easy imports: `from client import MCPClient`

## Quick Start

### Async Usage (Recommended)

```python
from client import MCPClient
import asyncio

async def main():
    async with MCPClient() as client:
        # Health check
        health = await client.health_check()
        print(f"Server status: {health['status']}")
        
        # Get schema for AI context
        schema = await client.get_schema_context()
        print(f"Schema: {schema[:100]}...")
        
        # Execute SQL
        result = await client.query_bigquery("SELECT 1 as test")
        print(f"Query result: {result}")

asyncio.run(main())
```

### Sync Usage (For Regular Scripts)

```python
from client import SyncMCPClient

# No async/await needed!
client = SyncMCPClient()

# Use directly
health = client.health_check()
schema = client.get_schema_context()
result = client.query_bigquery("SELECT 'Hello' as greeting")

print(f"Result: {result}")
```

## Available Methods

### Core Methods
- `call_tool(tool_name, arguments)` - Call any MCP tool
- `health_check()` - Check server health
- `get_schema_context()` - Get database schema
- `query_bigquery(query)` - Execute SQL queries

### Connection Management (Async only)
- `connect()` - Manual connection
- `disconnect()` - Manual disconnection
- Context manager (`async with`) - Automatic management

## Integration Examples

### 1. In a FastAPI Application

```python
from fastapi import FastAPI
from client import MCPClient

app = FastAPI()
mcp_client = None

@app.on_event("startup")
async def startup():
    global mcp_client
    mcp_client = MCPClient()
    await mcp_client.connect()

@app.on_event("shutdown")
async def shutdown():
    if mcp_client:
        await mcp_client.disconnect()

@app.get("/query")
async def query_data(sql: str):
    result = await mcp_client.query_bigquery(sql)
    return result
```

### 2. In a Jupyter Notebook

```python
# Cell 1: Setup
from client import SyncMCPClient
client = SyncMCPClient()

# Cell 2: Get schema
schema = client.get_schema_context()
print(schema)

# Cell 3: Run queries
result = client.query_bigquery("SELECT COUNT(*) FROM users")
print(result)
```

### 3. In an AI/LLM Application

```python
from client import MCPClient
import asyncio

async def nlp_to_sql_agent(user_question: str):
    async with MCPClient() as client:
        # Get schema context for AI
        schema = await client.get_schema_context()
        
        # Use your AI model to generate SQL from question + schema
        sql = generate_sql_from_question(user_question, schema)
        
        # Execute the query
        result = await client.query_bigquery(sql)
        
        # Format response for user
        return format_response(result)

# Usage
answer = asyncio.run(nlp_to_sql_agent("How many users do we have?"))
```

### 4. In a Data Science Script

```python
from client import SyncMCPClient
import pandas as pd

client = SyncMCPClient()

# Get data
result = client.query_bigquery("""
    SELECT user_id, order_count, total_amount 
    FROM user_analytics 
    WHERE created_date >= '2024-01-01'
""")

# Convert to DataFrame
df = pd.DataFrame(result['results'])
print(df.head())
```

## Error Handling

```python
from client import MCPClient

async def safe_query():
    try:
        async with MCPClient() as client:
            result = await client.query_bigquery("SELECT * FROM non_existent_table")
            return result
    except Exception as e:
        print(f"Query failed: {e}")
        return {"error": str(e)}
```

## Configuration

### Custom Server URL
```python
# Connect to different server
from client import MCPClient, SyncMCPClient

client = MCPClient("http://your-server:8000")

# Or sync version
sync_client = SyncMCPClient("http://your-server:8000")
```

## Performance Tips

1. **Use async version** for better performance in concurrent applications
2. **Reuse connections** when possible (manual connect/disconnect)
3. **Use context managers** for automatic cleanup
4. **Handle errors gracefully** for robust applications

## Testing Your Integration

Run the demo script to verify everything works:
```bash
cd client
python demo_client.py
```

Or run the complete test suite:
```bash
cd client
python test_client.py
```

Expected output should show successful health checks, schema retrieval, and query execution.

---

These clients make it easy to integrate your BigQuery MCP server into any Python application! 🚀
