"""
MCP Client Package

Lean, reusable clients for BigQuery MCP Server.

Available classes:
- MCPClient: Async client for async applications
- SyncMCPClient: Synchronous wrapper for regular Python scripts
"""

from .MCPClient import MCPClient
from .SyncMCPClient import SyncMCPClient

__version__ = "1.0.0"
__all__ = ["MCPClient", "SyncMCPClient"]
