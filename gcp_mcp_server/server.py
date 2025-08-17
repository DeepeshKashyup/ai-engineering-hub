from fastmcp import FastMCP
from controller.schema_context import get_schema_context
from google.cloud import bigquery
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials path from environment variable or use default
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', './credentials/gcp-practitioner.json')
# Convert to absolute path
credentials_path = str(Path(credentials_path).resolve())

# Set the credentials environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initialize BigQuery client
try:
    bq_client = bigquery.Client()
except Exception as e:
    print(f"Error initializing BigQuery client: {e}")
    print(f"Using credentials from: {credentials_path}")
    raise

mcp = FastMCP()


# Initialize FastMCP Server
mcp = FastMCP()

# Optional: Add a health check endpoint
@mcp.tool()
async def health_check():
    """Health check endpoint for the MCP server."""
    return {"status": "healthy"}

# Define the MCP endpoints
@mcp.tool()
def schema_context():
    """Returns the schema context for BigQuery tables.
    
    This tool provides metadata about available BigQuery tables, including their
    structure, columns, and relationships, helping the AI agent understand the
    data model for query generation.
    """
    return get_schema_context()

@mcp.tool()
async def query_bigquery(query: str):
    """Executes a BigQuery SQL query and returns the results.
    
    Args:
        query: The SQL query string to execute against BigQuery.
        
    Returns:
        A dictionary containing query results or an error message.
        Results are returned as a list of dictionaries, where each dictionary
        represents a row of data.
    """
    if not query:
        return {"error": "No query provided"}

    query_job = bq_client.query(query)
    results = query_job.result()
    return {"results": [dict(row) for row in results]}

# Get port from environment variable, default to 8000
port = int(os.getenv("PORT", 8000))
mcp.run(transport="http", host="0.0.0.0", port=port)