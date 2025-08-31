import dspy
from typing import List

class TableSelectorSignature(dspy.Signature):
    """Select relevant tables for a given user query."""
    user_query = dspy.InputField(desc="The user's natural language query")
    available_tables = dspy.InputField(desc="List of available table names")
    selected_tables = dspy.OutputField(desc="Comma-separated list of relevant table names")

class TableSelector(dspy.Module):
    def __init__(self, all_tables: List[str]):
        super().__init__()
        self.all_tables = all_tables
        self.selector = dspy.ChainOfThought(TableSelectorSignature)
    
    def forward(self, user_query: str) -> List[str]:
        tables_str = ", ".join(self.all_tables)
        result = self.selector(
            user_query=user_query,
            available_tables=tables_str
        )
        # Parse the comma-separated result
        selected = [table.strip() for table in result.selected_tables.split(",")]
        return [table for table in selected if table in self.all_tables]