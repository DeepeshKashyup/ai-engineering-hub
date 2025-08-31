import asyncio
from typing import List, Dict, Any

# ---------------------------
# MCP Database Client
# ---------------------------

class MCPClient:
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.use_real_mcp = True
        # Test if MCP tools are available
        try:
            from __main__ import mcp_my_gcp_server_schema_context, mcp_my_gcp_server_query_bigquery
            print("Real MCP tools detected and available")
        except ImportError:
            print("MCP tools not available, using fallback mode")
            self.use_real_mcp = False


    async def get_schema_and_rules(self, tables: List[str]) -> Dict[str, Any]:
        """Fetch schema and rules for a list of tables using actual MCP tools."""
        try:
            # Call the actual MCP tool to get schema information
            from __main__ import mcp_my_gcp_server_schema_context
            result = mcp_my_gcp_server_schema_context()
            
            # Parse the result to extract information for requested tables
            schema_info = {"schema": {}, "tables": tables}
            
            # The schema context returns information about all tables
            # Filter for the requested tables if needed
            schema_info["full_context"] = result
            schema_info["requested_tables"] = tables
            
            return schema_info
        except Exception as e:
            print(f"Error fetching schema from MCP: {e}")
            # Fallback to mock data if MCP call fails
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
                else:
                    mock_schema[table] = {
                        "columns": ["id", "name", "created_at"],
                        "primary_key": "id",
                        "description": f"Schema for {table} table"
                    }
            return {"schema": mock_schema, "tables": tables, "source": "fallback"}
    
    async def run_query(self, sql: str) -> Dict[str, Any]:
        """Execute SQL query using FastMCP."""
        try:
            # Mock implementation - in real version this would call:
            # result = await self.client.call_tool("execute_sql", {"query": sql})
            
            return {
                "query": sql,
                "status": "success",
                "rows": [
                    {"name": "John Doe", "city": "Lucknow", "total_spent": 6500},
                    {"name": "Jane Smith", "city": "Lucknow", "total_spent": 7200}
                ],
                "message": "Mock query execution successful"
            }
        except Exception as e:
            print(f"Error executing query: {e}")
            return {}
    
    async def list_tables(self) -> List[str]:
        """List all available tables."""
        try:
            # Mock implementation - in real version this would call:
            # result = await self.client.call_tool("list_tables", {})
            
            return ["customers", "orders", "products", "inventory", "users", "order_items"]
        except Exception as e:
            print(f"Error listing tables: {e}")
            return []
    
    def get_schema_and_rules_sync(self, tables: List[str]) -> Dict[str, Any]:
        """Synchronous wrapper for get_schema_and_rules."""
        return asyncio.run(self.get_schema_and_rules(tables))
    
    def run_query_sync(self, sql: str) -> Dict[str, Any]:
        """Synchronous wrapper for run_query."""
        return asyncio.run(self.run_query(sql))
    
    def list_tables_sync(self) -> List[str]:
        """Synchronous wrapper for list_tables."""
        return asyncio.run(self.list_tables())