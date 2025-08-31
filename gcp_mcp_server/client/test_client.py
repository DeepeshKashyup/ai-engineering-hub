
#!/usr/bin/env python3
"""
Test client for FastMCP BigQuery Server
Uses direct HTTP requests to test the FastMCP server
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, Any


class FastMCPTestClient:
    """Simple test client for FastMCP server"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = None
        self.session_id = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def initialize(self):
        """Initialize MCP session"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
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
                    print(f"✅ MCP session initialized. Session ID: {self.session_id}")
                    await self.send_initialized()
                    return True
                else:
                    print(f"❌ Failed to initialize: {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Error initializing: {e}")
            return False
    
    async def send_initialized(self):
        """Send initialized notification to complete the handshake"""
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
        except Exception as e:
            print(f"⚠️ Error sending initialized: {e}")
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None):
        """Call a tool via FastMCP"""
        if not self.session_id:
            return {"error": "No session ID"}
        
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
                    lines = content.strip().split('\n')
                    for line in lines:
                        if line.startswith('data: '):
                            data = line[6:]
                            try:
                                result = json.loads(data)
                                if "result" in result:
                                    tool_result = result["result"]
                                    if "content" in tool_result and tool_result["content"]:
                                        first_content = tool_result["content"][0]
                                        if "text" in first_content:
                                            return first_content["text"]
                                        else:
                                            return str(first_content)
                                    else:
                                        return tool_result
                                elif "error" in result:
                                    return {"error": result["error"]}
                                else:
                                    return result
                            except json.JSONDecodeError:
                                continue
                    return {"error": "No valid data found"}
                else:
                    error_text = await response.text()
                    return {"error": f"HTTP {response.status}: {error_text}"}
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}

async def test_tools():
    """Test all MCP tools"""
    print("🚀 FastMCP BigQuery Server Test Suite")
    print("=" * 50)
    
    async with FastMCPTestClient() as client:
        # Test 1: Health Check
        print("\n🧪 Testing Health Check...")
        response = await client.call_tool("health_check")
        if isinstance(response, dict) and "error" in response:
            print(f"❌ Health Check Failed: {response['error']}")
        else:
            print(f"✅ Health Check Success: {response}")
        
        # Test 2: Schema Context  
        print("\n📊 Testing Schema Context...")
        response = await client.call_tool("schema_context")
        if isinstance(response, dict) and "error" in response:
            print(f"❌ Schema Context Failed: {response['error']}")
        else:
            response_str = str(response)
            if len(response_str) > 300:
                print(f"✅ Schema Context Success ({len(response_str)} chars):")
                print(f"Preview: {response_str[:300]}...")
            else:
                print(f"✅ Schema Context Success: {response}")
        
        # Test 3: Simple BigQuery Query
        print("\n📈 Testing BigQuery Query...")
        test_query = "SELECT 1 as test_column, 'Hello World' as message"
        response = await client.call_tool("query_bigquery", {"query": test_query})
        if isinstance(response, dict) and "error" in response:
            print(f"❌ BigQuery Test Failed: {response['error']}")
        else:
            print(f"✅ BigQuery Test Success: {response}")
        
        print("\n" + "=" * 50)
        print("🏁 Testing Complete!")

if __name__ == "__main__":
    asyncio.run(test_tools())