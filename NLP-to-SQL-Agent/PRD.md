# Product: NLP-to-SQL Agent Dashboard

## Idea
An internal Streamlit web app for data analysts, business users, and managers to type natural language questions. An AI agent converts these into SQL queries, executed via an MCP server, and delivers results with AI-generated natural language insights.

## User Journey
1. User opens the Streamlit dashboard.
2. Types a natural language query into an input box.
3. AI agent (LangGraph + Azure OpenAI) identifies relevant database tables using schema context and converts the NL query into SQL.
4. SQL query is run via the run_big_query tool on the FastMCP server.
5. Results are displayed in a table on the dashboard.
6. AI-generated insights or summaries of the results are shown below the table.

## Target Audience
Internal teams: data analysts, business users, managers who lack direct visibility into database schema and want faster, simpler data access without writing SQL.

## Core Features
- Natural language input for queries
- AI-powered NL-to-SQL conversion with schema awareness
- Integration with MCP server’s run_big_query tool
- Result table display
- AI-generated natural language insights/summaries of results
- Minimal, clean, dashboard-style UI
- Live query-to-result flow with no persistent storage
- Solo user interaction (no collaboration)

## Tech Stack
- Streamlit (web app frontend)
- LangGraph + Azure OpenAI Chat (AI agent)
- FastMCP server with run_big_query tool (SQL execution)

## Design Vibe
Minimal, clean, dashboard-like — focused on clarity and usability.

## Future Features
- Saved queries and query history
- Role-based access and permissions
- Enhanced schema discovery and visualization
- Multi-language support
Product: NLP-to-SQL Agent Dashboard

Idea:
An internal Streamlit web app that lets data analysts, business users, and managers type natural language questions which an AI agent converts into SQL queries executed through an MCP server, delivering query results alongside AI-generated natural language insights.

User Journey:

User opens the Streamlit dashboard

Types a natural language query into an input box

AI agent (LangGraph + Azure OpenAI) identifies relevant database tables using schema context and converts the NL query into SQL

SQL query is run via the run_big_query tool on the FastMCP server

Results are displayed in a table on the dashboard

AI-generated insights or summaries of the results are shown below the table

Target Audience:
Internal teams: data analysts, business users, managers who lack direct visibility into database schema and want faster, simpler data access without writing SQL.

Core Features:

Natural language input for queries

AI-powered NL-to-SQL conversion with schema awareness

Integration with MCP server’s run_big_query tool

Result table display

AI-generated natural language insights/summaries of results

Minimal, clean, dashboard-style UI

Live query-to-result flow with no persistent storage

Solo user interaction (no collaboration)

Tech Stack:

Streamlit (web app frontend)

LangGraph + Azure OpenAI Chat (AI agent)

FastMCP server with run_big_query tool (SQL execution)

Design Vibe:
Minimal, clean, dashboard-like — focused on clarity and usability.

Future Features:

Saved queries and query history

Role-based access and permissions

Enhanced schema discovery and visualization

Multi-language support

More advanced AI-generated insights and recommendations