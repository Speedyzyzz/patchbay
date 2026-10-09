from typing import Any, Dict, Optional
import libcst as cst
from app.diff.change_taxonomy import APIContractChange, ChangeCategory

class CallSiteTransformer(cst.CSTTransformer):
    def __init__(self, target_symbol: str, change: APIContractChange):
        self.target_symbol = target_symbol
        self.change = change
        self.rewrites_performed = 0

    def leave_Call(self, original_node: cst.Call, updated_node: cst.Call) -> cst.Call:
        func_expr = cst.parse_module("").code_for_node(original_node.func).strip()
        method_name = func_expr.split(".")[-1] if "." in func_expr else func_expr

        # Match either exact symbol or method name
        if method_name != self.target_symbol and func_expr != self.target_symbol:
            return updated_node

        # 1. Handle Method Rename
        if self.change.category == ChangeCategory.ENDPOINT_RENAME and self.change.replacement_symbol:
            new_sym = self.change.replacement_symbol
            if isinstance(updated_node.func, cst.Attribute):
                new_func = updated_node.func.with_changes(attr=cst.Name(new_sym))
                self.rewrites_performed += 1
                return updated_node.with_changes(func=new_func)
            elif isinstance(updated_node.func, cst.Name):
                self.rewrites_performed += 1
                return updated_node.with_changes(func=cst.Name(new_sym))

        # 2. Handle Required Param Added
        elif self.change.category == ChangeCategory.PARAM_ADDED:
            param_name = self.change.new_signature.get("param", "version")
            default_val = self.change.new_signature.get("default", "'v2'")
            # Check if param already present
            existing_params = [
                a.keyword.value for a in updated_node.args if a.keyword is not None
            ]
            if param_name not in existing_params:
                new_arg = cst.Arg(
                    keyword=cst.Name(param_name),
                    value=cst.parse_expression(str(default_val)),
                    equal=cst.AssignEqual(whitespace_before=cst.SimpleWhitespace(""), whitespace_after=cst.SimpleWhitespace(""))
                )
                self.rewrites_performed += 1
                return updated_node.with_changes(args=[*updated_node.args, new_arg])

        return updated_node

class ASTRewriteSynthesizer:
    @staticmethod
    def apply_migration(source_code: str, change: APIContractChange) -> str:
        try:
            tree = cst.parse_module(source_code)
            transformer = CallSiteTransformer(change.target_symbol, change)
            modified_tree = tree.visit(transformer)
            return modified_tree.code
        except Exception:
            return source_code
