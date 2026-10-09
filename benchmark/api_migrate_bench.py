import sys
from pathlib import Path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from typing import Dict, Any, List
from app.diff.change_taxonomy import APIContractChange, ChangeCategory
from app.planner.rewrite_synthesizer import ASTRewriteSynthesizer
from app.verifier.runner import PatchVerifier

class APIMigrateBench:
    def __init__(self):
        self.total_tasks = 50
        self.typecheck_recovered = 0
        self.behavioral_passed = 0
        self.diff_ratios = []

    def run_rename_tasks(self) -> None:
        """15 Method/Endpoint renames"""
        for i in range(15):
            old_method = f"fetch_resource_{i}"
            new_method = f"get_resource_{i}"
            code = (
                f"# Module {i}\n"
                f"def handle_request():\n"
                f"    data = api_client.{old_method}(timeout=30)\n"
                f"    return data\n"
            )
            change = APIContractChange(
                change_id=f"rename_{i}",
                category=ChangeCategory.ENDPOINT_RENAME,
                target_symbol=old_method,
                replacement_symbol=new_method,
                migration_hint=f"Renamed {old_method} to {new_method}"
            )
            patched = ASTRewriteSynthesizer.apply_migration(code, change)
            report = PatchVerifier.verify_patch(code, patched)
            if report.typecheck_passed:
                self.typecheck_recovered += 1
            if report.behavioral_tests_passed:
                self.behavioral_passed += 1
            self.diff_ratios.append(report.minimal_diff_ratio)

    def run_param_addition_tasks(self) -> None:
        """15 Required parameter additions"""
        for i in range(15):
            method = f"create_record_{i}"
            code = (
                f"def submit(payload):\n"
                f"    return db_client.{method}(payload, immediate=True)\n"
            )
            change = APIContractChange(
                change_id=f"param_add_{i}",
                category=ChangeCategory.PARAM_ADDED,
                target_symbol=method,
                new_signature={"param": "tenant_id", "default": "'default-tenant'"},
                migration_hint="tenant_id required"
            )
            patched = ASTRewriteSynthesizer.apply_migration(code, change)
            report = PatchVerifier.verify_patch(code, patched)
            if report.typecheck_passed:
                self.typecheck_recovered += 1
            if report.behavioral_tests_passed:
                self.behavioral_passed += 1
            self.diff_ratios.append(report.minimal_diff_ratio)

    def run_pagination_tasks(self) -> None:
        """10 Pagination shifts"""
        for i in range(10):
            method = f"list_items_{i}"
            code = (
                f"def get_page():\n"
                f"    return store.{method}(category='all')\n"
            )
            change = APIContractChange(
                change_id=f"pagination_{i}",
                category=ChangeCategory.PARAM_ADDED,
                target_symbol=method,
                new_signature={"param": "cursor", "default": "None"},
                migration_hint="Cursor-based pagination"
            )
            patched = ASTRewriteSynthesizer.apply_migration(code, change)
            report = PatchVerifier.verify_patch(code, patched)
            if report.typecheck_passed:
                self.typecheck_recovered += 1
            if report.behavioral_tests_passed:
                self.behavioral_passed += 1
            self.diff_ratios.append(report.minimal_diff_ratio)

    def run_auth_change_tasks(self) -> None:
        """10 Authentication header/token structural changes"""
        for i in range(10):
            method = f"auth_request_{i}"
            code = (
                f"def authenticate():\n"
                f"    return gateway.{method}(api_key='token123')\n"
            )
            change = APIContractChange(
                change_id=f"auth_{i}",
                category=ChangeCategory.PARAM_ADDED,
                target_symbol=method,
                new_signature={"param": "bearer_auth", "default": "True"},
                migration_hint="bearer_auth flag added"
            )
            patched = ASTRewriteSynthesizer.apply_migration(code, change)
            report = PatchVerifier.verify_patch(code, patched)
            if report.typecheck_passed:
                self.typecheck_recovered += 1
            if report.behavioral_tests_passed:
                self.behavioral_passed += 1
            self.diff_ratios.append(report.minimal_diff_ratio)

    def execute_all_50_tasks(self) -> Dict[str, Any]:
        print("Running API-MigrateBench 50-Task Suite...")
        self.run_rename_tasks()
        self.run_param_addition_tasks()
        self.run_pagination_tasks()
        self.run_auth_change_tasks()

        typecheck_rate = (self.typecheck_recovered / self.total_tasks) * 100.0
        behavioral_rate = (self.behavioral_passed / self.total_tasks) * 100.0
        avg_diff_ratio = sum(self.diff_ratios) / len(self.diff_ratios)

        return {
            "total_tasks": self.total_tasks,
            "typecheck_recovery_rate": typecheck_rate,
            "behavioral_test_pass_rate": behavioral_rate,
            "average_minimal_diff_ratio": round(avg_diff_ratio, 3),
            "verdict": "BENCHMARK PASSED" if (typecheck_rate >= 90.0 and behavioral_rate >= 85.0 and avg_diff_ratio < 1.2) else "FAILED"
        }

def main():
    bench = APIMigrateBench()
    res = bench.execute_all_50_tasks()
    print("=" * 60)
    print(f"API-MIGRATEBENCH VERDICT: {res['verdict']}")
    print(f"Typecheck Recovery: {res['typecheck_recovery_rate']}% (Target: >90%)")
    print(f"Behavioral Test Pass Rate: {res['behavioral_test_pass_rate']}% (Target: >85%)")
    print(f"Avg Minimal Diff Ratio: {res['average_minimal_diff_ratio']} (Target: <1.2)")
    print("=" * 60)
    assert res["typecheck_recovery_rate"] >= 90.0
    assert res["behavioral_test_pass_rate"] >= 85.0
    assert res["average_minimal_diff_ratio"] < 1.2

if __name__ == "__main__":
    main()
