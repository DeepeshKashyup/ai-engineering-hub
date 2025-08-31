"""
Demo of the Cloud-Ready MCP Client
Shows how to configure the client for different deployment scenarios.
"""

import asyncio
from MCPClient_new import MCPClient, create_local_client, create_cloud_client, create_docker_client, create_mock_client

def demo_cloud_ready_mcp():
    """Demonstrate the cloud-ready MCP client with different configurations."""
    
    print("🌟 Cloud-Ready MCP Client Demo")
    print("=" * 50)
    
    # 1. Local Development
    print("\\n1️⃣ LOCAL DEVELOPMENT SETUP:")
    local_client = create_local_client()
    health = local_client.health_check_sync()
    print(f"   Health Check: {health}")
    
    # 2. Cloud Deployment
    print("\\n2️⃣ CLOUD DEPLOYMENT SETUP:")
    cloud_client = create_cloud_client("https://your-mcp-server.herokuapp.com")
    health = cloud_client.health_check_sync()
    print(f"   Health Check: {health}")
    
    # 3. Docker Deployment
    print("\\n3️⃣ DOCKER DEPLOYMENT SETUP:")
    docker_client = create_docker_client("mcp-bigquery-server", 8080)
    health = docker_client.health_check_sync()
    print(f"   Health Check: {health}")
    
    # 4. Mock/Testing
    print("\\n4️⃣ MOCK/TESTING SETUP:")
    mock_client = create_mock_client()
    health = mock_client.health_check_sync()
    print(f"   Health Check: {health}")
    
    # Demonstrate query execution with cloud client
    print("\\n🔍 TESTING QUERY EXECUTION:")
    print("   Using cloud client for sample query...")
    
    # Get available tables
    tables = cloud_client.list_tables_sync()
    print(f"   Available tables: {tables}")
    
    # Get schema for key tables
    schema_info = cloud_client.get_schema_and_rules_sync(["users", "orders"])
    print(f"   Schema source: {schema_info.get('source')}")
    print(f"   Server type: {schema_info.get('server_type')}")
    
    # Execute a sample query
    sample_query = """
    SELECT u.first_name, u.last_name, u.city, COUNT(o.order_id) as order_count
    FROM `bigquery-public-data.thelook_ecommerce.users` u
    LEFT JOIN `bigquery-public-data.thelook_ecommerce.orders` o ON u.id = o.user_id
    WHERE u.city = 'Lucknow'
    GROUP BY u.id, u.first_name, u.last_name, u.city
    HAVING COUNT(o.order_id) > 2
    ORDER BY order_count DESC
    LIMIT 10
    """
    
    result = cloud_client.run_query_sync(sample_query)
    print(f"   Query result source: {result.get('source')}")
    print(f"   Server URL: {result.get('server_url')}")
    print("   Sample results:")
    for row in result.get('rows', [])[:3]:  # Show first 3 rows
        print(f"     • {row}")
    
    # Show configuration options
    print("\\n⚙️ CONFIGURATION OPTIONS:")
    print("   For different deployment scenarios:")
    print("   • Local:     MCPClient('http://localhost:8000')")
    print("   • Cloud:     MCPClient('https://your-domain.com')")
    print("   • Docker:    MCPClient('http://mcp-server:8000')")
    print("   • Custom:    MCPClient('http://10.0.0.100:9000')")
    
    print("\\n🚀 DEPLOYMENT READY:")
    print("   ✅ Server URL configurable")
    print("   ✅ Cloud deployment supported") 
    print("   ✅ Docker-friendly")
    print("   ✅ Fallback to mock data")
    print("   ✅ Real MCP tools integration")

if __name__ == "__main__":
    demo_cloud_ready_mcp()
