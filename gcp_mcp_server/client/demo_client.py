#!/usr/bin/env python3
"""
Demo script showing how to use the lean MCPClient
"""

import asyncio

# Try relative import first, fall back to absolute
try:
    from .MCPClient import MCPClient
except ImportError:
    from MCPClient import MCPClient


async def demo_basic_usage():
    """Basic usage demonstration"""
    print("🔧 Basic MCPClient Usage Demo")
    print("-" * 40)
    
    async with MCPClient() as client:
        print("✅ Connected to MCP server")
        
        # 1. Health check
        print("\n1️⃣ Health Check:")
        health = await client.health_check()
        print(f"   Status: {health['status']}")
        
        # 2. Schema context
        print("\n2️⃣ Schema Context:")
        schema = await client.get_schema_context()
        lines = schema.split('\n')
        print(f"   Retrieved {len(schema)} characters")
        print(f"   First few lines:")
        for line in lines[:5]:
            print(f"   {line}")
        
        # 3. BigQuery queries
        print("\n3️⃣ BigQuery Queries:")
        
        # Simple query
        result1 = await client.query_bigquery("SELECT 'Hello' as greeting, 42 as answer")
        print(f"   Simple query result: {result1['results']}")
        
        # Math query
        result2 = await client.query_bigquery("SELECT 10 + 5 as sum, 10 * 5 as product")
        print(f"   Math query result: {result2['results']}")


async def demo_error_handling():
    """Error handling demonstration"""
    print("\n🛡️ Error Handling Demo")
    print("-" * 40)
    
    async with MCPClient() as client:
        # Test invalid query
        try:
            result = await client.query_bigquery("INVALID SQL QUERY")
            print(f"Unexpected success: {result}")
        except Exception as e:
            print(f"✅ Caught expected error: {e}")
        
        # Test invalid tool
        try:
            result = await client.call_tool("non_existent_tool")
            print(f"Unexpected success: {result}")
        except Exception as e:
            print(f"✅ Caught expected error: {e}")


async def demo_custom_queries():
    """Custom query demonstrations"""
    print("\n📊 Custom Query Demo")
    print("-" * 40)
    
    async with MCPClient() as client:
        queries = [
            ("Current timestamp", "SELECT CURRENT_DATETIME() as now"),
            ("String operations", "SELECT UPPER('hello world') as uppercase, LENGTH('test') as length"),
            ("Array operations", "SELECT [1, 2, 3, 4, 5] as numbers"),
            ("JSON operations", "SELECT JSON_OBJECT('name', 'John', 'age', 30) as person")
        ]
        
        for description, query in queries:
            try:
                result = await client.query_bigquery(query)
                print(f"   {description}: {result['results'][0]}")
            except Exception as e:
                print(f"   {description}: Error - {e}")


async def main():
    """Run all demos"""
    await demo_basic_usage()
    await demo_error_handling()
    await demo_custom_queries()
    
    print("\n🎉 Demo complete!")
    print("\n💡 Usage in your code:")
    print("""
    from MCPClient import MCPClient
    
    async def your_function():
        async with MCPClient() as client:
            # Get schema for AI context
            schema = await client.get_schema_context()
            
            # Execute SQL queries
            result = await client.query_bigquery("YOUR SQL HERE")
            
            return result
    """)


if __name__ == "__main__":
    asyncio.run(main())
