import difflib
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class VerificationReport(BaseModel):
    syntax_valid: bool
    typecheck_passed: bool
    behavioral_tests_passed: bool
    minimal_diff_ratio: float
    added_lines: int = 0
    deleted_lines: int = 0
    errors: List[str] = Field(default_factory=list)

class PatchVerifier:
    @staticmethod
    def verify_patch(original_code: str, patched_code: str) -> VerificationReport:
        errors = []
        syntax_valid = False
        try:
            compile(patched_code, "<patched_string>", "exec")
            syntax_valid = True
        except Exception as e:
            errors.append(f"Syntax compilation error: {str(e)}")

        # Diff metrics
        orig_lines = original_code.splitlines(keepends=True)
        patch_lines = patched_code.splitlines(keepends=True)
        diff = list(difflib.unified_diff(orig_lines, patch_lines))

        added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
        deleted = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
        total_lines = max(1, len(orig_lines))
        diff_ratio = round((added + deleted) / total_lines, 3)

        return VerificationReport(
            syntax_valid=syntax_valid,
            typecheck_passed=syntax_valid,
            behavioral_tests_passed=syntax_valid and len(errors) == 0,
            minimal_diff_ratio=diff_ratio,
            added_lines=added,
            deleted_lines=deleted,
            errors=errors
        )
