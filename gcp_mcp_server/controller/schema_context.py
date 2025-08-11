schema = {
    'users': {
        'columns': ['id', 'name', 'signup_date'],
        'relationships': {
            'orders': {'local_key': 'id', 'foreign_key': 'user_id'}
        }
    },
    'orders': {
        'columns': ['order_id', 'user_id', 'amount', 'created_at'],
        'relationships': {
            'users': {'local_key': 'user_id', 'foreign_key': 'id'}
        }
    }
}

sample_queries = {
    'users_orders_join': [
        "SELECT u.name, COUNT(o.order_id) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.name",
        "SELECT o.order_id, o.amount, u.name FROM orders o JOIN users u ON o.user_id = u.id WHERE o.amount > 100"
    ]
}

def get_schema_context():
    # Combine schema, relationships, and sample queries for the AI agent
    context_str = "Tables:\n"
    for tbl, info in schema.items():
        context_str += f"- {tbl}: columns {info['columns']}\n"
        for rel_tbl, rel_info in info['relationships'].items():
            context_str += f"  Relationship: {tbl}.{rel_info['local_key']} = {rel_tbl}.{rel_info['foreign_key']}\n"
    context_str += "\nSample queries:\n"
    for k, queries in sample_queries.items():
        for q in queries:
            context_str += f"{q}\n"
    return context_str