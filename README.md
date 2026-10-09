# PatchBay: Semantic API-Evolution & AST Migration Infrastructure

A compiler-adjacent platform that ingests upstream OpenAPI/SDK breaking-change diffs, maps affected call sites across monorepos using language ASTs (LibCST for Python and TypeScript Compiler AST), synthesizes minimal AST rewrites, and proves migrations through contract and behavioral tests.

## Architecture

- **`backend/app/parser/`**: AST indexer using LibCST to build a normalized repository API Usage Graph mapping call sites and callers.
- **`backend/app/diff/`**: OpenAPI and SDK contract change detector comparing vOld and vNew provider specifications (renames, parameter additions, pagination shifts, auth updates).
- **`backend/app/planner/`**: AST rewrite engine that synthesizes minimal, type-safe migration candidates preserving formatting and comments.
- **`backend/app/verifier/`**: Execution workers running typechecks, syntax compilation, and behavioral test suites.
- **`frontend/`**: Next.js 15 App Router API change feed, usage graph visualizer, and side-by-side patch review with automated PR branch creation.
- **`benchmark/`**: `API-MigrateBench` 50 breaking-change tasks measuring typecheck recovery rate (>90%), minimal-diff ratio (<1.2), and behavioral equivalence.

## Quick Start (Offline Verification)

```bash
# 1. Run all unit & integration tests (100% offline)
pytest backend/tests -v

# 2. Run the 50-task API-MigrateBench suite
python3 benchmark/api_migrate_bench.py
```

## Running Full Stack

```bash
# Start backend API (FastAPI)
cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8002

# Start frontend (Next.js 15)
cd frontend && npm install && npm run dev
```
