#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment from project root
project_root = Path(__file__).parent
env_path = project_root / '.env'
print(f"Loading .env from: {env_path}")
print(f".env exists: {env_path.exists()}")

load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY", "NOT_FOUND")
print(f"API Key loaded: {api_key[:20]}...")
print(f"Starts with sk-: {api_key.startswith('sk-')}")
print(f"Starts with sk-svcacct-: {api_key.startswith('sk-svcacct-')}")
