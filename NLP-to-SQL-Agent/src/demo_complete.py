"""
Complete NLP-to-SQL Demo with Cloud-Ready MCP Configuration
Shows how to use the configurable MCP client in a real scenario.
"""

from mcp_config import create_mcp_client_from_config, get_config, list_available_configs
import os

def demo_nlp_to_sql_with_cloud_mcp():
    """Demonstrate NLP-to-SQL with configurable MCP client."""
    
    print("🌟 NLP-to-SQL Agent with Cloud-Ready MCP")
    print("=" * 50)
    
    # Show available configurations
    print("\\n📋 Available MCP Configurations:")
    list_available_configs()
    
    # Create client based on environment (defaults to local)
    print("\\n🔧 Initializing MCP Client...")
    
    # You can set this via environment variable: 
    # export MCP_ENVIRONMENT=cloud_gcp
    # export MCP_SERVER_URL=https://your-actual-server.com
    
    client = create_mcp_client_from_config()  # Uses environment detection
    
    # Demonstrate the complete pipeline
    print("\\n🔍 Running NLP-to-SQL Pipeline:")
    user_query = "Show me customers from Mumbai who have placed more than 3 orders"
    print(f"   User Query: {user_query}")
    
    # Step 1: Health check
    print("\\n1️⃣ Health Check:")
    health = client.health_check_sync()
    print(f"   Server Status: {health.get('status')}")
    print(f"   Server Type: {health.get('server_type')}")
    print(f"   Data Source: {health.get('source')}")
    
    # Step 2: Get available tables
    print("\\n2️⃣ Available Tables:")
    tables = client.list_tables_sync()
    print(f"   Found {len(tables)} tables: {tables}")
    
    # Step 3: Select relevant tables (mock table selection)
    print("\\n3️⃣ Table Selection:")
    print("   Analyzing query for entities...")
    print("   - 'customers' → users table")
    print("   - 'orders' → orders table") 
    print("   - 'Mumbai' → city filter")
    selected_tables = ["users", "orders"]
    print(f"   Selected tables: {selected_tables}")
    
    # Step 4: Get schema information
    print("\\n4️⃣ Schema Information:")
    schema_info = client.get_schema_and_rules_sync(selected_tables)
    print(f"   Schema source: {schema_info.get('source')}")
    print(f"   Tables covered: {schema_info.get('tables', [])}")
    
    # Step 5: Generate SQL (mock SQL generation)
    print("\\n5️⃣ SQL Generation:")
    generated_sql = '''
    SELECT 
        u.first_name,
        u.last_name, 
        u.city,
        COUNT(o.order_id) as order_count
    FROM `bigquery-public-data.thelook_ecommerce.users` u
    JOIN `bigquery-public-data.thelook_ecommerce.orders` o ON u.id = o.user_id
    WHERE u.city = 'Mumbai'
    GROUP BY u.id, u.first_name, u.last_name, u.city
    HAVING COUNT(o.order_id) > 3
    ORDER BY order_count DESC
    LIMIT 10
    '''
    print("   Generated SQL:")
    print(generated_sql)
    
    # Step 6: Execute query
    print("\\n6️⃣ Query Execution:")
    result = client.run_query_sync(generated_sql)
    print(f"   Execution status: {result.get('status', 'unknown')}")
    print(f"   Data source: {result.get('source')}")
    print(f"   Server URL: {result.get('server_url')}")
    
    # Step 7: Show results
    print("\\n7️⃣ Results:")
    rows = result.get('rows', [])
    if rows:
        print(f"   Found {len(rows)} customers from Mumbai with >3 orders:")
        for i, row in enumerate(rows, 1):
            if isinstance(row, dict):
                name = row.get('name', 'Unknown')
                city = row.get('city', 'Unknown')
                count = row.get('total_spent', 'Unknown')  # Mock data structure
                print(f"   {i}. {name} from {city} - ₹{count}")
            else:
                print(f"   {i}. {row}")
    else:
        print("   No results found")
    
    # Step 8: Generate natural language answer
    print("\\n8️⃣ Natural Language Answer:")
    answer = f'''
    Based on your query about customers from Mumbai with more than 3 orders, 
    I found {len(rows)} customers who meet this criteria. 
    
    The analysis was performed using the {result.get('server_type', 'unknown')} MCP server 
    at {result.get('server_url', 'unknown location')}.
    
    Data source: {result.get('source', 'unknown')} implementation.
    '''
    print(answer)
    
    # Show deployment options
    print("\\n🚀 Deployment Options:")
    print("   To deploy this to different environments:")
    print("   • Local: Set MCP_ENVIRONMENT=local")
    print("   • GCP: Set MCP_ENVIRONMENT=cloud_gcp") 
    print("   • AWS: Set MCP_ENVIRONMENT=cloud_aws")
    print("   • Docker: Set MCP_ENVIRONMENT=docker_local")
    print("   • Custom: Set MCP_SERVER_URL=https://your-server.com")

def show_environment_examples():
    """Show how to configure for different environments."""
    print("\\n🌍 Environment Configuration Examples:")
    print("=" * 45)
    
    examples = {
        "Local Development": {
            "MCP_ENVIRONMENT": "local",
            "description": "Use local MCP server for development"
        },
        "Google Cloud": {
            "MCP_ENVIRONMENT": "cloud_gcp", 
            "MCP_SERVER_URL": "https://your-project.uc.r.appspot.com",
            "description": "Deploy to Google Cloud Platform"
        },
        "AWS Lambda": {
            "MCP_ENVIRONMENT": "cloud_aws",
            "MCP_SERVER_URL": "https://api.your-domain.com/mcp",
            "description": "Deploy to AWS with API Gateway"
        },
        "Docker": {
            "MCP_ENVIRONMENT": "docker_local",
            "description": "Use Docker container for MCP server"
        },
        "Custom Server": {
            "MCP_SERVER_URL": "https://mcp.your-company.com:8443",
            "MCP_USE_REAL": "true",
            "description": "Custom server deployment"
        }
    }
    
    for name, config in examples.items():
        print(f"\\n📦 {name}:")
        for key, value in config.items():
            if key != "description":
                print(f"   export {key}={value}")
        print(f"   # {config['description']}")

if __name__ == "__main__":
    demo_nlp_to_sql_with_cloud_mcp()
    show_environment_examples()
    
    print("\\n✨ Ready for Cloud Deployment! ✨")
    print("   Your NLP-to-SQL agent can now run on any cloud platform!")
