"""
Demo version of the NLP-to-SQL Agent without requiring OpenAI API key.
This version uses mock data to demonstrate the architecture.
"""

import asyncio
import sys
import os

# Add current directory to path to import MCPClient
sys.path.append(os.path.dirname(__file__))

try:
    from MCPClient import MCPClient
except ImportError:
    print("Error importing MCPClient. Creating a minimal version...")
    
    class MCPClient:
        def __init__(self, server_url: str = "http://localhost:8000"):
            self.server_url = server_url
        
        def list_tables_sync(self):
            return ["customers", "orders", "products", "inventory", "users", "order_items"]
        
        def get_schema_and_rules_sync(self, tables):
            mock_schema = {}
            for table in tables:
                if table == "customers":
                    mock_schema[table] = {
                        "columns": ["id", "name", "email", "city", "created_at"],
                        "primary_key": "id",
                        "description": "Customer information table"
                    }
                elif table == "orders":
                    mock_schema[table] = {
                        "columns": ["id", "customer_id", "amount", "status", "created_at"],
                        "primary_key": "id",
                        "foreign_keys": ["customer_id -> customers.id"],
                        "description": "Order transactions table"
                    }
            return {"schema": mock_schema, "tables": tables}
        
        def run_query_sync(self, sql):
            return {
                "query": sql,
                "status": "success",
                "rows": [
                    {"name": "John Doe", "city": "Lucknow", "total_spent": 6500},
                    {"name": "Jane Smith", "city": "Lucknow", "total_spent": 7200}
                ],
                "message": "Mock query execution successful"
            }

def demo_without_dspy():
    """Demo version that doesn't require DSPy/OpenAI to show the architecture."""
    
    print("🔍 User Query: Find the names of customers from Lucknow who spent more than 5000.")
    
    # Connect to MCP client
    client = MCPClient("http://localhost:8000")
    
    # Step 1: List available tables
    try:
        all_tables = client.list_tables_sync()
        print(f"📋 Available Tables: {all_tables}")
    except Exception as e:
        print(f"Could not fetch tables: {e}")
        all_tables = ["customers", "orders", "products", "inventory"]
    
    # Step 2: Mock table selection (normally done by TableSelector)
    print("📂 Table Selection Process:")
    print("   - Analyzing query for relevant entities...")
    print("   - Query mentions 'customers', 'Lucknow', 'spent'")
    print("   - Selected tables: customers, orders")
    selected_tables = ["customers", "orders"]
    
    # Step 3: Get schema information
    print("📊 Fetching Schema Information:")
    schema_info = client.get_schema_and_rules_sync(selected_tables)
    print(f"   - Schema retrieved for: {schema_info.get('tables', [])}")
    
    # Step 4: Mock SQL generation (normally done by NL2SQLAgent)
    print("🧠 SQL Generation Process:")
    print("   - Reasoning: Need to join customers and orders tables")
    print("   - Filter by city = 'Lucknow' and total spent > 5000")
    print("   - Group by customer to sum their total spending")
    
    mock_sql = """
    SELECT c.name, c.city, SUM(o.amount) as total_spent
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    WHERE c.city = 'Lucknow'
    GROUP BY c.id, c.name, c.city
    HAVING SUM(o.amount) > 5000
    ORDER BY total_spent DESC
    """
    print(f"📊 Generated SQL:\\n{mock_sql}")
    
    # Step 5: Execute query
    print("⚡ Executing Query:")
    results = client.run_query_sync(mock_sql)
    print(f"   - Status: {results.get('status')}")
    print(f"   - Message: {results.get('message')}")
    print("   - Results:")
    for row in results.get('rows', []):
        print(f"     • {row['name']} from {row['city']}: ₹{row['total_spent']}")
    
    # Step 6: Mock answer generation (normally done by AnswerAgent)
    print("💡 Answer Generation:")
    print("   - Converting results to natural language...")
    print("   - Found 2 customers meeting the criteria")
    
    final_answer = """
    Based on your query, I found 2 customers from Lucknow who have spent more than ₹5000:
    
    1. John Doe - Total spent: ₹6,500
    2. Jane Smith - Total spent: ₹7,200
    
    These customers have made multiple orders that sum up to more than your specified threshold of ₹5000.
    """
    
    print("✅ Final Answer:")
    print(final_answer)
    
    print("\\n🎯 Architecture Summary:")
    print("1. 📋 TableSelector → Selected relevant tables (customers, orders)")
    print("2. 🔍 MCPClient → Retrieved schema information")
    print("3. 🧠 NL2SQLAgent → Generated SQL with reasoning")
    print("4. ⚡ MCPClient → Executed query against database")
    print("5. 💡 AnswerAgent → Converted results to natural language")
    print("\\n✨ This demonstrates the complete NLP-to-SQL pipeline!")

if __name__ == "__main__":
    demo_without_dspy()
