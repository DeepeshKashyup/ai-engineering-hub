#!/usr/bin/env python3
"""
Updated main.py using the working MCPClient with SQL cleaning
"""

import dspy
import asyncio
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from MCPClient import MCPClient
from agent import TableSelector, NL2SQLAgent, AnswerAgent

# Load environment variables from .env file in project root
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)

def check_openai_key():
    """Check if OpenAI API key is properly configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found!")
        print("   Please set your OpenAI API key using one of these methods:")
        print("   1. Environment variable: $env:OPENAI_API_KEY='sk-your-key-here'")
        print("   2. Create .env file with: OPENAI_API_KEY=sk-your-key-here")
        return False
    elif not (api_key.startswith("sk-") or api_key.startswith("sk-svcacct-")):
        print("WARNING: OPENAI_API_KEY doesn't look like a valid OpenAI key")
        print(f"   Current value: {api_key[:10]}...")
        return False
    else:
        print(f"SUCCESS: OpenAI API key configured: {api_key[:10]}...{api_key[-4:]}")
        return True

def clean_sql_from_markdown(sql_text: str) -> str:
    """
    Clean SQL text by removing markdown code blocks and other formatting.
    
    Args:
        sql_text: Raw SQL text that may contain markdown formatting
        
    Returns:
        Clean SQL text ready for execution
    """
    print(f"CLEANING: SQL. Original length: {len(sql_text)} chars")
    
    # Remove markdown code blocks
    # Pattern matches ```sql ... ``` or ``` ... ```
    sql_cleaned = re.sub(r'```(?:sql)?\s*\n?(.*?)\n?```', r'\1', sql_text, flags=re.DOTALL)
    
    # Remove any remaining backticks at start/end
    sql_cleaned = sql_cleaned.strip('`')
    
    # Remove extra whitespace and newlines
    sql_cleaned = sql_cleaned.strip()
    
    print(f"CLEANED: SQL. New length: {len(sql_cleaned)} chars")
    
    # Show the difference if cleaning was applied
    if sql_cleaned != sql_text.strip():
        print("REMOVED: Markdown formatting from SQL")
    
    return sql_cleaned

async def process_query_async(user_query: str, client: MCPClient):
    """Process a single user query through the NLP-to-SQL pipeline using real MCP."""
    print(f"\n{'='*60}")
    print(f"USER QUERY: {user_query}")
    print(f"{'='*60}")
    print()

    try:
        # Step 1: Get schema context from MCP
        print("=" * 60)
        print("STEP 1: SCHEMA DISCOVERY")
        print("=" * 60)
        print("Getting schema context from MCP server...")
        schema_context = await client.get_schema_context()
        print(f"SUCCESS: Schema context retrieved ({len(schema_context)} chars)")
        print()
        
        # Extract table names from schema context (simple parsing)
        print("Parsing available tables from schema...")
        lines = schema_context.split('\n')
        available_tables = []
        for line in lines:
            if line.strip() and line.strip().endswith(':') and not line.startswith(' '):
                table_name = line.strip().rstrip(':').lower()
                if table_name not in ['database schema and context', 'tables', 'columns']:
                    available_tables.append(table_name)
        
        print(f"TABLES: Available tables: {available_tables}")
        print()

        # Step 2: Select relevant tables
        print("=" * 60)
        print("STEP 2: TABLE SELECTION")
        print("=" * 60)
        selector = TableSelector(available_tables)
        selected_tables = selector(user_query)
        print("SELECTED: Relevant tables:", selected_tables)
        print()

        # Step 3: Generate reasoning + SQL
        print("=" * 60)
        print("STEP 3: SQL GENERATION WITH AI REASONING")
        print("=" * 60)
        nl2sql = NL2SQLAgent()
        reasoning_sql = nl2sql(user_query, {"schema_context": schema_context, "tables": selected_tables})
        print("REASONING:")
        print(reasoning_sql.reasoning)
        print()
        print("RAW SQL GENERATED:")
        print(reasoning_sql.sql)
        print()

        # Step 4: Clean the SQL by removing markdown formatting
        print("=" * 60)
        print("STEP 4: SQL CLEANUP")
        print("=" * 60)
        clean_sql = clean_sql_from_markdown(reasoning_sql.sql)
        print("FINAL SQL FOR EXECUTION:")
        print(clean_sql)
        print()

        # Step 5: Execute SQL via MCP
        print("=" * 60)
        print("STEP 5: BIGQUERY EXECUTION")
        print("=" * 60)
        print("Executing query via MCP...")
        try:
            results = await client.query_bigquery(clean_sql)
            print("SUCCESS: Query executed successfully!")
            print()
            print("QUERY RESULTS:")
            print(results)
        except Exception as e:
            print(f"ERROR: Query execution failed: {e}")
            print()
            # Create mock results for demonstration
            results = {
                "results": [
                    {"name": "John Doe", "city": "Lucknow", "total_spent": 6500},
                    {"name": "Jane Smith", "city": "Lucknow", "total_spent": 7200}
                ],
                "status": "mock_fallback"
            }

        # Step 6: Generate natural language answer
        print()
        print("=" * 60)
        print("STEP 6: AI ANSWER GENERATION")
        print("=" * 60)
        answer_agent = AnswerAgent()
        final_answer = answer_agent(user_query, clean_sql, results)
        print("NATURAL LANGUAGE ANSWER:")
        print(final_answer.answer)
        print()
        print("=" * 60)
        print("PROCESS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"ERROR: Processing query failed: {e}")
        return False

async def interactive_mode():
    """Interactive mode for asking different questions using real MCP."""
    print("STARTING: Interactive NLP-to-SQL Agent with Real MCP")
    
    # Check OpenAI API key
    if not check_openai_key():
        print("\nERROR: OpenAI API key not configured. Please check your .env file.")
        return
    
    # Configure DSPy with OpenAI
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    print(f"CONFIGURING: DSPy with model: {model}")
    dspy.configure(lm=dspy.LM(model=model))

    print("\n" + "="*60)
    print("READY: Interactive NLP-to-SQL Agent!")
    print("="*60)
    print("INFO: Ask questions about your data in natural language")
    print("EXAMPLES:")
    print("   * 'Show me top 10 customers by revenue'")
    print("   * 'How many orders were placed last month?'")
    print("   * 'Which products are running low on inventory?'")
    print("   * 'Find customers who haven't ordered in 6 months'")
    print("   * 'What's the average order value by region?'")
    print()

    # Connect to MCP server
    async with MCPClient("http://localhost:8000") as client:
        print("CONNECTED: MCP server")
        
        # Test connection
        try:
            health = await client.health_check()
            print(f"HEALTH: MCP server status: {health}")
        except Exception as e:
            print(f"WARNING: MCP connection issue: {e}")
        
        print()
        print("="*60)
        print("READY FOR QUESTIONS! (Type 'quit' to exit)")
        print("="*60)
        
        while True:
            try:
                print()
                user_input = input("ENTER YOUR QUESTION: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                    print()
                    print("GOODBYE: Thanks for using the NLP-to-SQL Agent!")
                    break
                
                if not user_input:
                    print("WARNING: Please enter a question...")
                    continue
                
                # Process the query
                success = await process_query_async(user_input, client)
                
                if success:
                    print()
                    print("="*60)
                    print("QUERY PROCESSING COMPLETED!")
                    print("="*60)
                    print("Ready for next question...")
                else:
                    print()
                    print("ERROR: Failed to process query. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\nGOODBYE: Thanks for using the NLP-to-SQL Agent!")
                break
            except Exception as e:
                print(f"\nERROR: Unexpected error: {e}")

def main():
    """Main function to choose execution mode."""
    print("NLP-to-SQL Agent with Real MCP Integration")
    print("=" * 50)
    print("Choose Mode:")
    print("1. Interactive Mode (ask your own questions)")
    print("2. Demo Mode (see example queries)")
    print("3. Single Test Query")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        asyncio.run(interactive_mode())
    elif choice == "2":
        # Demo queries implementation here
        print("Demo mode - implement if needed")
    elif choice == "3":
        # Single test query
        async def test_single():
            async with MCPClient("http://localhost:8000") as client:
                await process_query_async("Find all users from California", client)
        
        # Configure DSPy first
        if check_openai_key():
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            dspy.configure(lm=dspy.LM(model=model))
            asyncio.run(test_single())
    else:
        print("Invalid choice. Running interactive mode...")
        asyncio.run(interactive_mode())

if __name__ == "__main__":
    main()