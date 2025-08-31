#!/usr/bin/env python3
"""
FastMCP Test Client for BigQuery MCP Server

This client connects to the FastMCP server using the correct protocol.
"""

import asyncio
import aiohttp
import json
import sys
from typing import Dict, Any, Optional
import argparse
from datetime import datetime

class FastMCPClient:
    """Client for connecting to FastMCP server via SSE"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
        self.session_id: Optional[str] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def initialize(self) -> Dict[str, Any]:
        """Initialize MCP session"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "1",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            async with self.session.post(
                f"{self.base_url}/mcp",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    # Read SSE response
                    async for line in response.content:
                        line = line.decode().strip()
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: ' prefix
                            try:
                                result = json.loads(data)
                                # Extract session ID from response
                                if "sessionId" in str(result):
                                    # Look for session ID in the response
                                    response_str = json.dumps(result)
                                    import re
                                    match = re.search(r'"sessionId":"([^"]+)"', response_str)
                                    if match:
                                        self.session_id = match.group(1)
                                        print(f"Session ID extracted: {self.session_id}")
                                return result
                            except json.JSONDecodeError:
                                continue
                else:
                    return {"error": f"HTTP {response.status}: {await response.text()}"}
        except Exception as e:
            return {"error": f"Initialize failed: {str(e)}"}
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "2",
                "method": "tools/list"
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            # Add session ID if available
            if self.session_id:
                headers["X-Session-ID"] = self.session_id
            
            async with self.session.post(
                f"{self.base_url}/mcp",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    async for line in response.content:
                        line = line.decode().strip()
                        if line.startswith('data: '):
                            data = line[6:]
                            try:
                                return json.loads(data)
                            except json.JSONDecodeError:
                                continue
                else:
                    return {"error": f"HTTP {response.status}: {await response.text()}"}
        except Exception as e:
            return {"error": f"List tools failed: {str(e)}"}
    
    async def call_tool(self, name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a tool"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "id": "3",
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": arguments or {}
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
            
            # Add session ID if available
            if self.session_id:
                headers["X-Session-ID"] = self.session_id
            
            async with self.session.post(
                f"{self.base_url}/mcp",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    async for line in response.content:
                        line = line.decode().strip()
                        if line.startswith('data: '):
                            data = line[6:]
                            try:
                                result = json.loads(data)
                                return result
                            except json.JSONDecodeError:
                                continue
                else:
                    return {"error": f"HTTP {response.status}: {await response.text()}"}
        except Exception as e:
            return {"error": f"Tool call failed: {str(e)}"}

class FastMCPTester:
    """Test suite for FastMCP server functionality"""
    
    def __init__(self, client: FastMCPClient):
        self.client = client
        self.results = []
    
    def log_test(self, test_name: str, success: bool, result: Any, details: str = ""):
        """Log test results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        status = "✅ PASS" if success else "❌ FAIL"
        self.results.append({
            "timestamp": timestamp,
            "test": test_name,
            "success": success,
            "result": result,
            "details": details
        })
        print(f"[{timestamp}] {status} {test_name}")
        if details:
            print(f"         {details}")
        if not success and isinstance(result, dict) and "error" in result:
            print(f"         Error: {result['error']}")
    
    async def test_initialize(self):
        """Test MCP initialization"""
        print("\n🔗 Testing MCP Initialization...")
        result = await self.client.initialize()
        success = "result" in result and "capabilities" in result.get("result", {})
        
        if success:
            caps = result["result"]["capabilities"]
            details = f"Server capabilities: {list(caps.keys())}"
        else:
            details = result.get("error", "Unknown error")
        
        self.log_test("MCP Initialize", success, result, details)
        return success
    
    async def test_list_tools(self):
        """Test tools listing"""
        print("\n🛠️ Testing Tools List...")
        result = await self.client.list_tools()
        success = "result" in result and "tools" in result.get("result", {})
        
        if success:
            tools = result["result"]["tools"]
            details = f"Found {len(tools)} tools"
            print("     Available tools:")
            for tool in tools:
                print(f"       - {tool.get('name', 'unknown')}: {tool.get('description', 'no description')}")
        else:
            details = result.get("error", "Unknown error")
        
        self.log_test("Tools List", success, result, details)
        return success
    
    async def test_health_check(self):
        """Test health check tool"""
        print("\n❤️ Testing Health Check...")
        result = await self.client.call_tool("health_check")
        success = "result" in result and not result.get("error")
        
        if success:
            tool_result = result.get("result", {})
            if "content" in tool_result:
                content = tool_result["content"]
                if content and len(content) > 0:
                    first_content = content[0]
                    if "text" in first_content:
                        details = f"Health status: {first_content['text']}"
                    else:
                        details = "Health check returned content"
                else:
                    details = "Health check completed"
            else:
                details = "Health check completed"
        else:
            details = result.get("error", "Unknown error")
        
        self.log_test("Health Check", success, result, details)
        return success
    
    async def test_schema_context(self):
        """Test schema context retrieval"""
        print("\n📊 Testing Schema Context...")
        result = await self.client.call_tool("schema_context")
        success = "result" in result and not result.get("error")
        
        if success:
            tool_result = result.get("result", {})
            if "content" in tool_result:
                content = tool_result["content"]
                if content and len(content) > 0:
                    first_content = content[0]
                    if "text" in first_content:
                        schema_text = first_content["text"]
                        details = f"Schema context length: {len(schema_text)} characters"
                        
                        # Show a snippet
                        snippet = schema_text[:300] + "..." if len(schema_text) > 300 else schema_text
                        print(f"     Schema preview:\n{snippet}")
                    else:
                        details = "Schema context returned"
                else:
                    details = "Empty schema context"
            else:
                details = "Schema context completed"
        else:
            details = result.get("error", "Unknown error")
        
        self.log_test("Schema Context", success, result, details)
        return success
    
    async def test_simple_query(self):
        """Test a simple BigQuery query"""
        print("\n📈 Testing Simple BigQuery Query...")
        
        test_query = "SELECT 1 as test_column, 'Hello World' as message"
        result = await self.client.call_tool("query_bigquery", {"query": test_query})
        success = "result" in result and not result.get("error")
        
        if success:
            tool_result = result.get("result", {})
            if "content" in tool_result:
                content = tool_result["content"]
                if content and len(content) > 0:
                    first_content = content[0]
                    if "text" in first_content:
                        try:
                            query_result = json.loads(first_content["text"])
                            if "results" in query_result:
                                details = f"Query returned {len(query_result['results'])} rows"
                                print(f"     Query: {test_query}")
                                print(f"     Results: {query_result['results']}")
                            else:
                                details = "Query executed but no results key found"
                        except json.JSONDecodeError:
                            details = "Query returned non-JSON response"
                    else:
                        details = "Query completed"
                else:
                    details = "Empty query result"
            else:
                details = "Query completed"
        else:
            details = result.get("error", "Unknown error")
        
        self.log_test("Simple BigQuery Query", success, result, details)
        return success
    
    def print_summary(self):
        """Print test summary"""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"\n{'='*60}")
        print(f"🏁 TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.results:
                if not result["success"]:
                    print(f"   - {result['test']}: {result.get('details', 'No details')}")
        
        print(f"\n{'='*60}")

async def run_tests(server_url: str):
    """Run all tests against the FastMCP server"""
    
    print("🚀 BigQuery FastMCP Server Test Suite")
    print(f"📡 Server URL: {server_url}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    async with FastMCPClient(server_url) as client:
        tester = FastMCPTester(client)
        
        # Run tests in sequence
        init_ok = await tester.test_initialize()
        
        if init_ok:
            await tester.test_list_tools()
            await tester.test_health_check()
            await tester.test_schema_context()
            await tester.test_simple_query()
        else:
            print("❌ Initialization failed - skipping other tests")
        
        # Print summary
        tester.print_summary()
        
        # Return success status
        return all(r["success"] for r in tester.results)

async def interactive_mode(server_url: str):
    """Interactive mode for manual testing"""
    print("🔧 Interactive Mode - Enter tool names to test")
    print("Commands: 'health_check', 'schema_context', 'query <SQL>', 'quit'")
    print("-" * 50)
    
    async with FastMCPClient(server_url) as client:
        # Initialize first
        init_result = await client.initialize()
        if "error" in init_result:
            print(f"❌ Failed to initialize: {init_result['error']}")
            return
        
        print("✅ MCP session initialized")
        
        while True:
            try:
                command = input("\n> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    break
                elif command.lower() == 'health_check':
                    result = await client.call_tool("health_check")
                    print(json.dumps(result, indent=2))
                elif command.lower() == 'schema_context':
                    result = await client.call_tool("schema_context")
                    print(json.dumps(result, indent=2))
                elif command.startswith('query '):
                    sql = command[6:].strip()
                    result = await client.call_tool("query_bigquery", {"query": sql})
                    print(json.dumps(result, indent=2))
                elif command.lower() == 'tools':
                    result = await client.list_tools()
                    print(json.dumps(result, indent=2))
                elif command:
                    # Try to call it as a tool
                    result = await client.call_tool(command)
                    print(json.dumps(result, indent=2))
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Test client for BigQuery FastMCP Server")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="MCP server URL (default: http://localhost:8000)")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Run in interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive:
        asyncio.run(interactive_mode(args.url))
    else:
        success = asyncio.run(run_tests(args.url))
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
