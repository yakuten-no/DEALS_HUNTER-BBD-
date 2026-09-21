# BBD HUNTER — Current State

> Purpose: the exact current state of the project. Update after every meaningful implementation change.
> Last updated: 2026-09-21 (session date; container UTC clock read 2026-09-20T22:25Z) · Memory layer V0.1

**STATE CONFIDENCE: LOW.** The repository was not available when this file was written. Only what was directly observed is marked `[VERIFIED]`.

## Current version
- Target phase: **V0.1 (foundation)**.
- Version of the code actually present: `[UNKNOWN]`.
- Project memory layer: V0.1 (created 2026-09-21).

## What is working
- `[VERIFIED]` `project-memory/` exists with 14 Markdown files.
- No application feature is confirmed working.

## Partially implemented
- `[UNKNOWN]` Whether any V0.1 scaffold (frontend shell, backend shell, database shell, config, dashboard, health endpoint, wishlist model, docs) exists elsewhere, for example on the user's machine or in another AI session.

## Not implemented (as far as verified)
No BBD HUNTER application code was found in the memory-creation environment. So, as far as anything inspected shows: no frontend, backend, database, collectors, deal engine, AI layer, notifications, automation or tests. This means "not found", not "confirmed absent from the project".

## Current development objective
1. Reconcile this memory with the real repository (T-001).
2. Finish the V0.1 foundation. No scraping, no checkout automation.

## Current blockers
- The repository was not accessible in the session that created this memory. Fix: give an agent the repository (upload it, or run the agent inside it), then follow `MEMORY_PROTOCOL.md` rule 14.
- Open questions that will need decisions: `ARCHITECTURE.md` section 11.

## Important files
| Path | What it is | Status |
|---|---|---|
| `project-memory/AI_CONTEXT.md` | Primary AI handoff | `[VERIFIED]` exists |
| `project-memory/` (other `.md` files and `KNOWLEDGE/`) | The rest of the memory layer | `[VERIFIED]` exist |
| Master Project Instructions | User-authored goals, philosophy, stack, V0.1 scope | Exists (user-authored); location in the repo `[UNKNOWN]` |
| Application source directories | Intended layout is in `ARCHITECTURE.md` | `[UNKNOWN]` |

## Last meaningful change
2026-09-21 — created the project memory layer (`project-memory/`). No code changes.

## How this state was determined (inspection log, 2026-09-21)
Checked in the memory-creation environment:
- Uploads folder: empty. Earlier-transcripts folder: empty. Working directory: no project files (tool caches only).
- Filesystem search outside system and dependency directories for names containing `bbd`, `hunter` or `project-memory`; for `.git` directories; and for `package.json`, `pyproject.toml`, `requirements.txt`, `vite.config.*`, `main.py`: nothing belonging to BBD HUNTER.
- Conclusion: there was no repository to inspect. Nothing was invented to fill the gap.
