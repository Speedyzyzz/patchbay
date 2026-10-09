from app.parser.python_cst import PythonASTIndexer

def test_ast_indexer_extracts_call_sites():
    code = (
        "def process():\n"
        "    a = client.fetch_orders(active=True)\n"
        "    b = client.get_users()\n"
        "    return a + b\n"
    )

    graph = PythonASTIndexer.index_source(code, "services/orders.py")
    assert len(graph.call_sites) == 2
    symbols = [cs.symbol_name for cs in graph.call_sites]
    assert "fetch_orders" in symbols
    assert "get_users" in symbols
    assert "fetch_orders" in graph.symbol_to_files
    assert graph.symbol_to_files["fetch_orders"] == ["services/orders.py"]
