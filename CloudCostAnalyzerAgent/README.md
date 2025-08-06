# Cloud Cost Analyzer Agent

## Problem statement

Cloud cost often spirals due to underutilized resources, lack of automated cleanup and poor visibility. We need an agent that:

- Identifies underutilized resources
- Understands user queries (e.g, "why is the GCP bill high this month")
- Runs actual gcloud CLI commands using an authenticated MCP tool 
- summarizes findings and suggests actions

## Cloud Cost optimization Agent (Langchain + MCP)

✅ Langchain Components:
- **LLM**: OpenAI GPT-4
- **orchestration**: Langchain
- **tools**: MCP tool for executing gcloud commands
