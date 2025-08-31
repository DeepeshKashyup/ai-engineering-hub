import dspy
import asyncio
import os
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
        print("❌ OPENAI_API_KEY not found!")
        print("   Please set your OpenAI API key using one of these methods:")
        print("   1. Environment variable: $env:OPENAI_API_KEY='sk-your-key-here'")
        print("   2. Create .env file with: OPENAI_API_KEY=sk-your-key-here")
        return False
    elif not (api_key.startswith("sk-") or api_key.startswith("sk-svcacct-")):
        print("⚠️  Warning: OPENAI_API_KEY doesn't look like a valid OpenAI key")
        print(f"   Current value: {api_key[:10]}...")
        return False
    else:
        print(f"✅ OpenAI API key configured: {api_key[:10]}...{api_key[-4:]}")
        return True

def process_query(user_query: str, client: MCPClient, all_tables: list):
    """Process a single user query through the NLP-to-SQL pipeline."""
    print(f"\n{'='*60}")
    print(f"🔍 User Query: {user_query}")
    print(f"{'='*60}")

    try:
        # Step 1: Select relevant tables
        selector = TableSelector(all_tables)
        selected_tables = selector(user_query)
        print("📂 Relevant Tables:", selected_tables)

        # Step 2: Fetch schema + rules for selected tables
        schema_and_rules = client.get_schema_and_rules_sync(selected_tables)
        print("📊 Schema Info:", schema_and_rules)

        # Step 3: Generate reasoning + SQL
        nl2sql = NL2SQLAgent()
        reasoning_sql = nl2sql(user_query, schema_and_rules)
        print("🧠 Reasoning:\n", reasoning_sql.reasoning)
        print("📊 SQL Generated:\n", reasoning_sql.sql)

        # Step 4: Execute SQL via FastMCP
        results = client.run_query_sync(reasoning_sql.sql)
        print("📂 Results:\n", results)

        # Step 5: Summarize answer
        answer_agent = AnswerAgent()
        final_answer = answer_agent(user_query, reasoning_sql.sql, results)
        print("💡 Final Answer:\n", final_answer.answer)
        
        return True
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        return False

def interactive_mode():
    """Interactive mode for asking different questions."""
    print("🚀 Starting Interactive NLP-to-SQL Agent")
    
    # Check OpenAI API key
    if not check_openai_key():
        print("\n🔄 Running in mock mode without real AI...")
        return
    
    # Configure DSPy with OpenAI
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    print(f"🤖 Configuring DSPy with model: {model}")
    dspy.configure(lm=dspy.LM(model=model))

    # Connect FastMCP client
    client = MCPClient("http://localhost:8000")

    # Get available tables
    try:
        all_tables = client.list_tables_sync()
        print("📋 Available Tables:", all_tables)
    except Exception as e:
        print(f"Could not fetch tables: {e}")
        all_tables = ["customers", "orders", "products", "inventory", "users", "transactions", "sales"]

    print("\n" + "="*60)
    print("🎯 Interactive NLP-to-SQL Agent Ready!")
    print("="*60)
    print("💡 Ask questions about your data in natural language")
    print("📝 Examples:")
    print("   • 'Show me top 10 customers by revenue'")
    print("   • 'How many orders were placed last month?'")
    print("   • 'Which products are running low on inventory?'")
    print("   • 'Find customers who haven't ordered in 6 months'")
    print("   • 'What's the average order value by region?'")
    print("\n💬 Type your question (or 'quit' to exit):")

    while True:
        try:
            user_input = input("\n🤔 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q', 'bye']:
                print("👋 Goodbye! Thanks for using the NLP-to-SQL Agent!")
                break
            
            if not user_input:
                print("⚠️  Please enter a question...")
                continue
            
            # Process the query
            success = process_query(user_input, client, all_tables)
            
            if success:
                print("\n✅ Query processed successfully!")
            else:
                print("\n❌ Failed to process query. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using the NLP-to-SQL Agent!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

def demo_queries():
    """Run a set of demo queries to showcase different question types."""
    print("🚀 Running Demo Queries")
    
    # Check OpenAI API key
    if not check_openai_key():
        print("\n🔄 Running in mock mode without real AI...")
        return
    
    # Configure DSPy with OpenAI
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    print(f"🤖 Configuring DSPy with model: {model}")
    dspy.configure(lm=dspy.LM(model=model))

    # Connect FastMCP client
    client = MCPClient("http://localhost:8000")

    # Get available tables
    try:
        all_tables = client.list_tables_sync()
        print("📋 Available Tables:", all_tables)
    except Exception as e:
        print(f"Could not fetch tables: {e}")
        all_tables = ["customers", "orders", "products", "inventory", "users", "transactions", "sales"]

    # Demo queries
    demo_questions = [
        "Find the names of customers from Lucknow who spent more than 5000",
        "Show me the top 5 best-selling products this quarter",
        "How many new customers joined last month?",
        "Which products are out of stock or running low?",
        "What's the total revenue for each region?",
        "Find customers who have made more than 10 orders",
        "Show me the average order value by customer segment"
    ]

    print(f"\n🎬 Running {len(demo_questions)} demo queries...")
    
    for i, question in enumerate(demo_questions, 1):
        print(f"\n🎯 Demo Query {i}/{len(demo_questions)}")
        process_query(question, client, all_tables)
        
        if i < len(demo_questions):
            input("\n⏸️  Press Enter to continue to next query...")

if __name__ == "__main__":
    print("🎯 NLP-to-SQL Agent - Choose Mode:")
    print("1. Interactive Mode (ask your own questions)")
    print("2. Demo Mode (see example queries)")
    print("3. Single Query Mode (original)")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        interactive_mode()
    elif choice == "2":
        demo_queries()
    elif choice == "3":
        # Original single query mode
        from main import run_sync
        run_sync()
    else:
        print("Invalid choice. Running interactive mode...")
        interactive_mode()