#!/usr/bin/env python3
"""Test script to verify knowledge base functionality."""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from controller.schema_context import get_schema_context, initialize_gcs_config

def test_local_knowledge_base():
    """Test loading from local knowledge base."""
    print("Testing local knowledge base...")
    context = get_schema_context()
    print("\n=== Schema Context ===")
    print(context)
    print("\n" + "="*50)

def test_gcs_knowledge_base():
    """Test loading from GCS bucket (if configured)."""
    print("\nTesting GCS knowledge base configuration...")
    # This would require actual GCS bucket setup
    test_bucket = "gs://example-bucket/knowledge-base"
    initialize_gcs_config(test_bucket)
    print(f"GCS configuration initialized for: {test_bucket}")
    print("Note: Actual GCS access would require valid credentials and bucket")

if __name__ == "__main__":
    test_local_knowledge_base()
    test_gcs_knowledge_base()
