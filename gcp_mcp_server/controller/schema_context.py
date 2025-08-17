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

# Default schema data (fallback)
default_schema = {
    'users': {
        'columns': ['id', 'name', 'signup_date'],
        'relationships': {
            'orders': {'local_key': 'id', 'foreign_key': 'user_id'}
        }
    },
    'orders': {
        'columns': ['order_id', 'user_id', 'amount', 'created_at'],
        'relationships': {
            'users': {'local_key': 'user_id', 'foreign_key': 'id'}
        }
    }
}

default_sample_queries = {
    'users_orders_join': [
        "SELECT u.name, COUNT(o.order_id) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.name",
        "SELECT o.order_id, o.amount, u.name FROM orders o JOIN users u ON o.user_id = u.id WHERE o.amount > 100"
    ]
}

def load_knowledge_base_from_local(knowledge_base_dir: str = "knowledge_base") -> Dict[str, Any]:
    """Load knowledge base files from local directory."""
    schema_data = {}
    sample_queries_data = {}
    
    try:
        # Get absolute path to knowledge base directory
        kb_path = Path(knowledge_base_dir)
        if not kb_path.is_absolute():
            # If relative path, make it relative to the script's directory
            script_dir = Path(__file__).parent.parent
            kb_path = script_dir / kb_path
        
        if not kb_path.exists():
            print(f"Knowledge base directory not found: {kb_path}")
            return {"schema": default_schema, "sample_queries": default_sample_queries}
        
        # Load schema files
        schema_file = kb_path / "schema.json"
        if schema_file.exists():
            with open(schema_file, 'r') as f:
                schema_data = json.load(f)
        
        # Load sample queries files
        queries_file = kb_path / "sample_queries.json"
        if queries_file.exists():
            with open(queries_file, 'r') as f:
                sample_queries_data = json.load(f)
        
        # Use default data if files are empty or missing
        if not schema_data:
            schema_data = default_schema
        if not sample_queries_data:
            sample_queries_data = default_sample_queries
            
    except Exception as e:
        print(f"Error loading local knowledge base: {e}")
        schema_data = default_schema
        sample_queries_data = default_sample_queries
    
    return {"schema": schema_data, "sample_queries": sample_queries_data}

def load_knowledge_base_from_gcs() -> Dict[str, Any]:
    """Load knowledge base files from GCS bucket."""
    if not gcs_client or not gcs_bucket_path:
        print("GCS client or bucket path not configured")
        return {"schema": default_schema, "sample_queries": default_sample_queries}
    
    schema_data = {}
    sample_queries_data = {}
    
    try:
        # Parse bucket path (format: gs://bucket-name/path/to/knowledge_base or bucket-name/path)
        bucket_path_clean = gcs_bucket_path.replace('gs://', '')
        path_parts = bucket_path_clean.split('/', 1)
        bucket_name = path_parts[0]
        prefix = path_parts[1] if len(path_parts) > 1 else ""
        
        bucket = gcs_client.bucket(bucket_name)
        
        # Load schema from GCS
        schema_blob_name = f"{prefix}/schema.json" if prefix else "schema.json"
        schema_blob = bucket.blob(schema_blob_name)
        if schema_blob.exists():
            schema_content = schema_blob.download_as_text()
            schema_data = json.loads(schema_content)
        
        # Load sample queries from GCS
        queries_blob_name = f"{prefix}/sample_queries.json" if prefix else "sample_queries.json"
        queries_blob = bucket.blob(queries_blob_name)
        if queries_blob.exists():
            queries_content = queries_blob.download_as_text()
            sample_queries_data = json.loads(queries_content)
        
        # Use default data if files are empty or missing
        if not schema_data:
            schema_data = default_schema
        if not sample_queries_data:
            sample_queries_data = default_sample_queries
            
    except Exception as e:
        print(f"Error loading knowledge base from GCS: {e}")
        schema_data = default_schema
        sample_queries_data = default_sample_queries
    
    return {"schema": schema_data, "sample_queries": sample_queries_data}

def get_schema_context():
    """Get schema context from knowledge base (local or GCS) or fallback to default."""
    # Try to load from GCS if configured, otherwise load from local
    if gcs_bucket_path and gcs_client:
        print(f"Loading knowledge base from GCS bucket: {gcs_bucket_path}")
        knowledge_base = load_knowledge_base_from_gcs()
    else:
        print("Loading knowledge base from local directory")
        knowledge_base = load_knowledge_base_from_local()
    
    schema = knowledge_base["schema"]
    sample_queries = knowledge_base["sample_queries"]
    
    # Combine schema, relationships, and sample queries for the AI agent
    context_str = "Tables:\n"
    for tbl, info in schema.items():
        context_str += f"- {tbl}: columns {info['columns']}\n"
        if 'relationships' in info:
            for rel_tbl, rel_info in info['relationships'].items():
                context_str += f"  Relationship: {tbl}.{rel_info['local_key']} = {rel_tbl}.{rel_info['foreign_key']}\n"
    
    context_str += "\nSample queries:\n"
    for k, queries in sample_queries.items():
        if isinstance(queries, list):
            for q in queries:
                context_str += f"{q}\n"
        else:
            context_str += f"{queries}\n"
    
    return context_str