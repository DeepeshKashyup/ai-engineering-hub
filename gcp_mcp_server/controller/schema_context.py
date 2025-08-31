import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from google.cloud import storage

# Global variables to store GCS configuration
gcs_bucket_path = None
gcs_client = None

def initialize_gcs_config(bucket_path: Optional[str] = None):
    """Initialize GCS configuration if bucket path is provided."""
    global gcs_bucket_path, gcs_client
    if bucket_path:
        gcs_bucket_path = bucket_path
        try:
            gcs_client = storage.Client()
        except Exception as e:
            print(f"Error initializing GCS client for knowledge base: {e}")
            gcs_client = None

# Default database context (fallback)
default_database_context = {
    "tables": {
        "users": {
            "columns": [
                {"name": "id", "type": "INTEGER", "description": "Primary key"},
                {"name": "name", "type": "STRING", "description": "User full name"},
                {"name": "signup_date", "type": "DATE", "description": "Account creation date"}
            ],
            "relationships": {
                "orders": {"local_key": "id", "foreign_key": "user_id"}
            },
            "sample_data": [
                {"id": 1, "name": "John Doe", "signup_date": "2024-01-15"},
                {"id": 2, "name": "Jane Smith", "signup_date": "2024-02-20"}
            ]
        },
        "orders": {
            "columns": [
                {"name": "order_id", "type": "INTEGER", "description": "Primary key"},
                {"name": "user_id", "type": "INTEGER", "description": "Foreign key to users"},
                {"name": "amount", "type": "DECIMAL", "description": "Order amount"},
                {"name": "created_at", "type": "TIMESTAMP", "description": "Creation time"}
            ],
            "relationships": {
                "users": {"local_key": "user_id", "foreign_key": "id"}
            },
            "sample_data": [
                {"order_id": 101, "user_id": 1, "amount": 150.00, "created_at": "2024-03-01T10:30:00Z"},
                {"order_id": 102, "user_id": 2, "amount": 75.50, "created_at": "2024-03-02T14:15:00Z"}
            ]
        }
    },
    "sample_queries": {
        "user_orders": {
            "description": "Get user order counts",
            "sql": "SELECT u.name, COUNT(o.order_id) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.name"
        }
    }
}


def load_knowledge_base_from_local(knowledge_base_dir: str = "knowledge_base") -> Dict[str, Any]:
    """Load knowledge base files from local Json file."""
    #schema_data = {}
    #sample_queries_data = {}
    
    try:
        # Get absolute path to knowledge base directory
        kb_path = Path(knowledge_base_dir)
        if not kb_path.is_absolute():
            # If relative path, make it relative to the script's directory
            script_dir = Path(__file__).parent.parent
            kb_path = script_dir / kb_path
        
        if not kb_path.exists():
            print(f"Knowledge base directory not found: {kb_path}")
            #return {"schema": default_schema, "sample_queries": default_sample_queries}
            return default_database_context
        
        # Load unified database context file
        context_file = kb_path / "database_context.json"
        if context_file.exists():
            with open(context_file, 'r') as f:
                return json.load(f)
        else:
            print(f"Database context file not found: {context_file}")
            return default_database_context
            
    except Exception as e:
        print(f"Error loading local database base: {e}")
        return default_database_context

def load_knowledge_base_from_gcs() -> Dict[str, Any]:
    """Load knowledge base files from GCS bucket."""
    if not gcs_client or not gcs_bucket_path:
        print("GCS client or bucket path not configured")
        return default_database_context

    try:
        # Parse bucket path (format: gs://bucket-name/path/to/knowledge_base or bucket-name/path)
        bucket_path_clean = gcs_bucket_path.replace('gs://', '')
        path_parts = bucket_path_clean.split('/', 1)
        bucket_name = path_parts[0]
        prefix = path_parts[1] if len(path_parts) > 1 else ""
        
        bucket = gcs_client.bucket(bucket_name)
        
        # Load unified database context from GCS
        context_blob_name = f"{prefix}/database_context.json" if prefix else "database_context.json"
        context_blob = bucket.blob(context_blob_name)

        if context_blob.exists():
            context_content = context_blob.download_as_text()
            return json.loads(context_content)
        else:
            print(f"Database context file not found in GCS: {context_blob_name}")
            return default_database_context

    except Exception as e:
        print(f"Error loading knowledge base from GCS: {e}")
        return default_database_context
    
def get_schema_context():
    """Get comprehensive database context including schema, sample data, and queries."""
    # Load from GCS if configured, otherwise load from local
    if gcs_bucket_path and gcs_client:
        print(f"Loading database context from GCS bucket: {gcs_bucket_path}")
        db_context = load_knowledge_base_from_gcs()
    else:
        print("Loading database context from local directory")
        db_context = load_knowledge_base_from_local()

    # Generate comprehensive context string
    context_str = "DATABASE SCHEMA AND CONTEXT:\n\n"
    
    # Tables section
    context_str += "TABLES:\n"
    for table_name, table_info in db_context.get("tables", {}).items():
        context_str += f"\n{table_name.upper()}:\n"
        context_str += "  Columns:\n"
        
        for col in table_info.get("columns", []):
            if isinstance(col, dict):
                desc = f" - {col.get('description', '')}" if col.get('description') else ""
                context_str += f"    - {col['name']} ({col.get('type', 'UNKNOWN')}){desc}\n"
            else:
                context_str += f"    - {col}\n"
        
        # Relationships
        if table_info.get("relationships"):
            context_str += "  Relationships:\n"
            for rel_table, rel_info in table_info["relationships"].items():
                context_str += f"    - {table_name}.{rel_info['local_key']} = {rel_table}.{rel_info['foreign_key']}\n"
        
        # Sample data
        if table_info.get("sample_data"):
            context_str += "  Sample Data:\n"
            for i, row in enumerate(table_info["sample_data"][:3]):  # Show max 3 rows
                context_str += f"    Row {i+1}: {row}\n"
    
    # Sample queries section
    context_str += "\nSAMPLE QUERIES:\n"
    for query_name, query_info in db_context.get("sample_queries", {}).items():
        if isinstance(query_info, dict):
            desc = query_info.get("description", "")
            sql = query_info.get("sql", "")
            context_str += f"\n{query_name.upper()}:\n"
            if desc:
                context_str += f"  Description: {desc}\n"
            context_str += f"  SQL: {sql}\n"
        else:
            context_str += f"{query_name}: {query_info}\n"
    
    return context_str