

User Query 
   ↓
TableSelector (decides which tables are relevant) 
   ↓
MCP tools (fetch schema + rules for only those tables) 
   ↓
NL2SQLAgent (reasoning → SQL) 
   ↓
MCP.execute_sql (run query) 
   ↓
AnswerAgent (summarize results in natural language)