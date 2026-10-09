from fastapi import APIRouter
from pydantic import BaseModel
from app.diff.change_taxonomy import APIContractChange
from app.planner.rewrite_synthesizer import ASTRewriteSynthesizer
from app.verifier.runner import PatchVerifier

router = APIRouter(prefix="/migrations", tags=["Migrations"])

class MigrationRequest(BaseModel):
    source_code: str
    change: APIContractChange

@router.post("/synthesize")
async def synthesize_and_verify(req: MigrationRequest):
    patched_code = ASTRewriteSynthesizer.apply_migration(req.source_code, req.change)
    report = PatchVerifier.verify_patch(req.source_code, patched_code)
    return {
        "original_code": req.source_code,
        "patched_code": patched_code,
        "verification_report": report.model_dump()
    }
