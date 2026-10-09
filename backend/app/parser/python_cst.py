from pathlib import Path
from typing import List, Optional
import libcst as cst
from app.parser.usage_graph import APIUsageGraph, CallSite

class PythonCallSiteVisitor(cst.CSTVisitor):
    def __init__(self, file_path: str, usage_graph: APIUsageGraph):
        self.file_path = file_path
        self.usage_graph = usage_graph
        self.current_line = 1

    def visit_Call(self, node: cst.Call) -> Optional[bool]:
        # Extract callee expression as code
        callee_expr = cst.parse_module("").code_for_node(node.func).strip()
        args_repr = [cst.parse_module("").code_for_node(a).strip() for a in node.args]

        # Extract symbol name (e.g. "client.get_user" -> "get_user" or full attribute)
        symbol = callee_expr.split(".")[-1] if "." in callee_expr else callee_expr

        self.usage_graph.add_call_site(
            CallSite(
                file_path=self.file_path,
                line_number=self.current_line,
                symbol_name=symbol,
                callee_expression=callee_expr,
                arguments=args_repr
            )
        )
        return True

class PythonASTIndexer:
    @staticmethod
    def index_source(source_code: str, file_path: str = "main.py") -> APIUsageGraph:
        graph = APIUsageGraph()
        try:
            tree = cst.parse_module(source_code)
            visitor = PythonCallSiteVisitor(file_path, graph)
            tree.visit(visitor)
        except Exception:
            pass  # Fallback for unparseable syntax
        return graph

    @staticmethod
    def index_directory(directory: str) -> APIUsageGraph:
        graph = APIUsageGraph()
        dir_path = Path(directory)
        for py_file in dir_path.rglob("*.py"):
            try:
                code = py_file.read_text(encoding="utf-8")
                tree = cst.parse_module(code)
                visitor = PythonCallSiteVisitor(str(py_file), graph)
                tree.visit(visitor)
            except Exception:
                continue
        return graph
