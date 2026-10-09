from typing import Any, Dict, List
from app.diff.change_taxonomy import APIContractChange, ChangeCategory

class OpenAPIDiffDetector:
    @staticmethod
    def compare_specs(old_spec: Dict[str, Any], new_spec: Dict[str, Any]) -> List[APIContractChange]:
        changes: List[APIContractChange] = []
        old_paths = old_spec.get("paths", {})
        new_paths = new_spec.get("paths", {})

        # 1. Detect Endpoint Renames and Removals
        for path, path_item in old_paths.items():
            if path not in new_paths:
                # Look for matching rename in new_paths
                possible_rename = None
                for n_path, n_item in new_paths.items():
                    if n_item.get("summary") == path_item.get("summary"):
                        possible_rename = n_path
                        break

                if possible_rename:
                    changes.append(
                        APIContractChange(
                            change_id=f"rename_{path}",
                            category=ChangeCategory.ENDPOINT_RENAME,
                            target_symbol=path,
                            replacement_symbol=possible_rename,
                            old_signature={"path": path},
                            new_signature={"path": possible_rename},
                            migration_hint=f"Endpoint renamed from {path} to {possible_rename}"
                        )
                    )

        # 2. Detect Parameter Changes on common paths
        for path in old_paths:
            if path in new_paths:
                old_ops = old_paths[path]
                new_ops = new_paths[path]
                for method, old_op in old_ops.items():
                    if method in new_ops:
                        new_op = new_ops[method]
                        old_params = {p["name"]: p for p in old_op.get("parameters", [])}
                        new_params = {p["name"]: p for p in new_op.get("parameters", [])}

                        # Required param added
                        for p_name, p_info in new_params.items():
                            if p_name not in old_params and p_info.get("required", False):
                                changes.append(
                                    APIContractChange(
                                        change_id=f"param_added_{path}_{p_name}",
                                        category=ChangeCategory.PARAM_ADDED,
                                        target_symbol=f"{method.upper()} {path}",
                                        old_signature={},
                                        new_signature={"param": p_name, "type": p_info.get("type", "string")},
                                        migration_hint=f"Required parameter '{p_name}' added to {method.upper()} {path}"
                                    )
                                )

                        # Pagination changes: if page/limit replaced with cursor
                        if "page" in old_params and "cursor" in new_params:
                            changes.append(
                                APIContractChange(
                                    change_id=f"pagination_{path}",
                                    category=ChangeCategory.PAGINATION_CHANGED,
                                    target_symbol=f"{method.upper()} {path}",
                                    old_signature={"type": "offset", "params": ["page", "limit"]},
                                    new_signature={"type": "cursor", "params": ["cursor"]},
                                    migration_hint="Pagination model shifted from page/limit offset to cursor-based token"
                                )
                            )

        return changes
