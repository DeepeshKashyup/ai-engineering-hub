#!/usr/bin/env python3
"""
Synchronous wrapper for MCPClient

Provides sync methods for easier integration with non-async code.
"""

import asyncio
from typing import Dict, Any

# Try relative import first, fall back to absolute
try:
    from .MCPClient import MCPClient
except ImportError:
    from MCPClient import MCPClient


class SyncMCPClient:
    """Synchronous wrapper for MCPClient"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize sync MCP client
        
        Args:
            base_url: Base URL of the MCP server
        """
        self.base_url = base_url
        self._loop = None
    
    def _run_async(self, coro):
        """Run async coroutine in sync context"""
        try:
            # Try to get existing event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, we need a new thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(asyncio.run, coro)
                    return future.result()
            else:
                return loop.run_until_complete(coro)
        except RuntimeError:
            # No event loop, create new one
            return asyncio.run(coro)
    
    async def _async_call_tool(self, tool_name: str, arguments: Dict[str, Any] = None):
        """Async helper for tool calls"""
        async with MCPClient(self.base_url) as client:
            return await client.call_tool(tool_name, arguments)
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Any:
        """
        Call an MCP tool synchronously
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments (optional)
            
        Returns:
            Tool response data
        """
        return self._run_async(self._async_call_tool(tool_name, arguments))
    
    def health_check(self) -> dict:
        """Check server health (synchronous)"""
        async def _health():
            async with MCPClient(self.base_url) as client:
                return await client.health_check()
        
        return self._run_async(_health())
    
    def get_schema_context(self) -> str:
        """Get database schema context (synchronous)"""
        async def _schema():
            async with MCPClient(self.base_url) as client:
                return await client.get_schema_context()
        
        return self._run_async(_schema())
    
    def query_bigquery(self, query: str) -> dict:
        """Execute BigQuery SQL query (synchronous)"""
        async def _query():
            async with MCPClient(self.base_url) as client:
                return await client.query_bigquery(query)
        
        return self._run_async(_query())


# Example usage
def demo_sync_client():
    """Demo of synchronous client usage"""
    print("🔄 Synchronous MCPClient Demo")
    print("-" * 40)
    
    # Create sync client
    client = SyncMCPClient()
    
    # Health check
    print("1️⃣ Health Check:")
    health = client.health_check()
    print(f"   Status: {health['status']}")
    
    # Schema context
    print("\n2️⃣ Schema Context:")
    schema = client.get_schema_context()
    print(f"   Length: {len(schema)} characters")
    
    # Query
    print("\n3️⃣ BigQuery Query:")
    result = client.query_bigquery("SELECT 'Sync client works!' as message, 123 as number")
    print(f"   Result: {result['results'][0]}")


if __name__ == "__main__":
    demo_sync_client()
