from app.planner.rewrite_synthesizer import ASTRewriteSynthesizer
from app.diff.change_taxonomy import APIContractChange, ChangeCategory
from app.verifier.runner import PatchVerifier

def test_ast_rewrite_method_rename():
    code = (
        "# Important comment to preserve\n"
        "res = client.get_users(limit=10)\n"
        "print(res)\n"
    )

    change = APIContractChange(
        change_id="c1",
        category=ChangeCategory.ENDPOINT_RENAME,
        target_symbol="get_users",
        replacement_symbol="list_users",
        migration_hint="Renamed to list_users"
    )

    patched = ASTRewriteSynthesizer.apply_migration(code, change)
    assert "client.list_users(limit=10)" in patched
    assert "# Important comment to preserve" in patched  # Preserves comments!

    # Verification passes
    report = PatchVerifier.verify_patch(code, patched)
    assert report.syntax_valid is True
    assert report.typecheck_passed is True
    assert report.minimal_diff_ratio <= 1.0

def test_ast_rewrite_add_required_param():
    code = (
        "data = client.fetch_records(user_id=42)\n"
    )

    change = APIContractChange(
        change_id="c2",
        category=ChangeCategory.PARAM_ADDED,
        target_symbol="fetch_records",
        new_signature={"param": "api_version", "default": "'2026-01'"},
        migration_hint="api_version required"
    )

    patched = ASTRewriteSynthesizer.apply_migration(code, change)
    assert "api_version='2026-01'" in patched
    assert "user_id=42" in patched

    report = PatchVerifier.verify_patch(code, patched)
    assert report.syntax_valid is True
