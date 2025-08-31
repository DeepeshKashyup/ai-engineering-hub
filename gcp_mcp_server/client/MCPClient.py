#!/usr/bin/env python3
"""
Lean MCP Client for FastMCP BigQuery Server

A simple, reusable client class for calling MCP tools.
Can be imported and used in other applications.
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, Optional


class MCPClient:
    """Lean MCP client for FastMCP servers"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize MCP client
        
        Args:
            base_url: Base URL of the MCP server (default: http://localhost:8000)
        """
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
        self.session_id: Optional[str] = None
        self.initialized = False
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
    
    async def connect(self):
        """Connect to MCP server and initialize session"""
        if self.session:
            return
        
        self.session = aiohttp.ClientSession()
        
        # Initialize MCP session
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "mcp-client", "version": "1.0.0"}
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        try:
            async with self.session.post(f"{self.base_url}/mcp", json=payload, headers=headers) as response:
                if response.status == 200:
                    self.session_id = response.headers.get('mcp-session-id')
                    await self._send_initialized()
                    self.initialized = True
                else:
                    raise Exception(f"Failed to initialize MCP session: HTTP {response.status}")
        except Exception as e:
            await self.disconnect()
            raise Exception(f"MCP connection failed: {e}")
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.session:
            await self.session.close()
            self.session = None
        self.session_id = None
        self.initialized = False
    
    async def _send_initialized(self):
        """Send initialized notification to complete MCP handshake"""
        if not self.session_id:
            return
        
        payload = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "mcp-session-id": self.session_id
        }
        
        try:
            async with self.session.post(f"{self.base_url}/mcp", json=payload, headers=headers) as response:
                pass  # Notification doesn't require response handling
        except Exception:
            pass  # Non-critical error
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Any:
        """
        Call an MCP tool
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments (optional)
            
        Returns:
            Tool response data
            
        Raises:
            Exception: If not connected or tool call fails
        """
        if not self.initialized:
            raise Exception("MCP client not connected. Use 'await client.connect()' or context manager.")
        
        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "mcp-session-id": self.session_id
        }
        
        try:
            async with self.session.post(f"{self.base_url}/mcp", json=payload, headers=headers) as response:
                if response.status == 200:
                    content = await response.text()
                    return self._parse_sse_response(content)
                else:
                    error_text = await response.text()
                    raise Exception(f"Tool call failed: HTTP {response.status} - {error_text}")
        except Exception as e:
            raise Exception(f"Tool '{tool_name}' call failed: {e}")
    
    def _parse_sse_response(self, content: str) -> Any:
        """Parse Server-Sent Events response"""
        lines = content.strip().split('\n')
        for line in lines:
            if line.startswith('data: '):
                data = line[6:]  # Remove 'data: ' prefix
                try:
                    result = json.loads(data)
                    if "result" in result:
                        tool_result = result["result"]
                        if "content" in tool_result and tool_result["content"]:
                            first_content = tool_result["content"][0]
                            if "text" in first_content:
                                return first_content["text"]
                            else:
                                return first_content
                        else:
                            return tool_result
                    elif "error" in result:
                        raise Exception(f"Tool error: {result['error']}")
                    else:
                        return result
                except json.JSONDecodeError:
                    continue
        
        raise Exception("No valid response data found")
    
    # Convenience methods for common tools
    async def health_check(self) -> dict:
        """Check server health"""
        result = await self.call_tool("health_check")
        return json.loads(result) if isinstance(result, str) else result
    
    async def get_schema_context(self) -> str:
        """Get database schema context"""
        return await self.call_tool("schema_context")
    
    async def query_bigquery(self, query: str) -> dict:
        """Execute BigQuery SQL query"""
        result = await self.call_tool("query_bigquery", {"query": query})
        return json.loads(result) if isinstance(result, str) else result


# Example usage functions
async def example_usage():
    """Example of how to use the MCPClient"""
    print("🔌 Connecting to MCP server...")
    
    # Method 1: Using context manager (recommended)
    async with MCPClient() as client:
        # Health check
        health = await client.health_check()
        print(f"Server health: {health}")
        
        # Get schema context
        schema = await client.get_schema_context()
        print(f"Schema context length: {len(schema)} characters")
        
        # Execute query
        result = await client.query_bigquery("SELECT 1 as test, 'Hello' as message")
        print(f"Query result: {result}")

async def example_manual_connection():
    """Example of manual connection management"""
    client = MCPClient()
    
    try:
        await client.connect()
        
        # Use the client
        health = await client.health_check()
        print(f"Health: {health}")
        
    finally:
        await client.disconnect()


if __name__ == "__main__":
    # Run example
    print("🚀 MCP Client Example")
    asyncio.run(example_usage())
