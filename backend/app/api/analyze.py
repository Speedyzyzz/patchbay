from typing import Any, Dict
from fastapi import APIRouter
from pydantic import BaseModel
from app.diff.openapi_diff import OpenAPIDiffDetector
from app.parser.python_cst import PythonASTIndexer

router = APIRouter(prefix="/analyze", tags=["Analyze"])

class ContractDiffRequest(BaseModel):
    old_spec: Dict[str, Any]
    new_spec: Dict[str, Any]

class RepoAnalysisRequest(BaseModel):
    source_code: str
    file_path: str = "main.py"

@router.post("/contract")
async def analyze_contract(req: ContractDiffRequest):
    changes = OpenAPIDiffDetector.compare_specs(req.old_spec, req.new_spec)
    return {"total_changes": len(changes), "changes": [c.model_dump() for c in changes]}

@router.post("/repo")
async def analyze_repo(req: RepoAnalysisRequest):
    graph = PythonASTIndexer.index_source(req.source_code, req.file_path)
    return graph.model_dump()
