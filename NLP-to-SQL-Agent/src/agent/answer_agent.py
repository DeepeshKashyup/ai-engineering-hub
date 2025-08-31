import dspy
from typing import Dict, Any

class AnswerSignature(dspy.Signature):
    """Summarize SQL query results in natural language."""
    user_query = dspy.InputField(desc="The original user query")
    sql_query = dspy.InputField(desc="The SQL query that was executed")
    query_results = dspy.InputField(desc="Results from the SQL query")
    answer = dspy.OutputField(desc="Natural language summary of the results")

class AnswerAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.summarizer = dspy.ChainOfThought(AnswerSignature)
    
    def forward(self, user_query: str, sql_query: str, results: Dict[str, Any]):
        result = self.summarizer(
            user_query=user_query,
            sql_query=sql_query,
            query_results=str(results)
        )
        return result