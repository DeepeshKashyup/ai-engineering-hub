import dspy
from typing import Dict, Any

class NL2SQLSignature(dspy.Signature):
    """Convert natural language query to SQL with reasoning."""
    user_query = dspy.InputField(desc="The user's natural language query")
    schema_info = dspy.InputField(desc="Database schema and rules for relevant tables")
    reasoning = dspy.OutputField(desc="Step-by-step reasoning for the SQL query")
    sql = dspy.OutputField(desc="The generated SQL query")

class NL2SQLAgent(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generator = dspy.ChainOfThought(NL2SQLSignature)
    
    def forward(self, user_query: str, schema_and_rules: Dict[str, Any]):
        schema_str = str(schema_and_rules)
        result = self.generator(
            user_query=user_query,
            schema_info=schema_str
        )
        return result