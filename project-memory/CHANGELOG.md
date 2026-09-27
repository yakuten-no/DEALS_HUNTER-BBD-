# BBD HUNTER — Changelog

> Purpose: meaningful project changes, newest first. Add an entry after every meaningful change (see `MEMORY_PROTOCOL.md`).
> Last updated: 2026-09-26 · Memory layer V0.1

Entry format: `## YYYY-MM-DD — Version or phase — title`, then Added / Changed / Fixed / Removed as needed.

## 2026-09-26 — V0.1 — foundation implementation built
### Added
- Backend (`backend/`): FastAPI app, environment-variable configuration, SQLite + SQLModel database layer, a real (non-hardcoded) `GET /api/health` check, full wishlist CRUD (`POST/GET/GET-by-id/PUT/DELETE /api/wishlists`) with request validation, 18 pytest tests.
- Frontend (`frontend/`): React + TypeScript + Vite + Tailwind dashboard — hunt input (natural-language box plus an optional manual "exact constraints" panel), wishlist panel wired to the real backend, live system-status panel, honest empty-state deal feed, session activity log, 8 Vitest tests.
- Root `README.md`: setup, run, and test instructions for both Windows and macOS/Linux, plus an explicit note on what was and wasn't verifiable in the sandboxed build environment.
- `collectors/README.md`, `ai/README.md`, `automation/README.md`, `database/README.md`, `tests/README.md`: each empty-for-now folder explains what will eventually live there and why it's empty now.
- Five new architectural decisions recorded: D-013 (SQLModel, no migrations yet), D-014 (PUT as partial update), D-015 (test placement), D-016 (Tailwind v3, no Framer Motion in V0.1), D-017 (visual design system reasoning).

### Changed
- `project-memory/ARCHITECTURE.md`: added §12 "Actual layout (V0.1)" with the real file tree; updated the component-status table, the frontend/backend interface description (REST + polling, not WebSocket, in V0.1), the technology-choices table, and resolved/updated several open architectural questions (OQ-1 and OQ-9 resolved for V0.1; OQ-5 noted as deliberately deferred).
- `project-memory/CURRENT_STATE.md`: fully rewritten from direct repository inspection (previously written with no repository available).
- `project-memory/AI_CONTEXT.md`: fully rewritten to reflect the above.
- `project-memory/TODO.md`: marked T-001, T-002, T-010 through T-019, and T-032 done; added T-003/T-004 (run it for real; fix what that surfaces) and T-020 (wire up an edit UI for wishlists); noted T-044 (introduce a migration tool before real data is at stake).
- `project-memory/REQUIREMENTS.md`: updated the V0.1 scope table's status column from `[UNVERIFIED]` to `[BUILT]` for each item now implemented.
- `project-memory/ROADMAP.md`: updated the V0.1 status line.
- `project-memory/MEMORY_PROTOCOL.md`: formally documented the new `[BUILT]` status tag (written and passed offline checks, not yet run live) used throughout this update.

### Notes
- Built entirely in a sandboxed environment with **no network access** (confirmed: `pip` and `npm` registry requests both failed). Nothing here has actually been installed or run yet — see `CURRENT_STATE.md` for exactly what offline verification was possible (Python syntax via `py_compile`: clean; TypeScript/TSX syntax via the TypeScript compiler's own parser: clean across 18 files) and what remains to be confirmed by an actual run.
- No retailer scraping, checkout automation, CAPTCHA/OTP handling, or AI integration was implemented, per this phase's explicit instructions.

## 2026-09-21 — Project Memory Layer V0.1 — memory layer created
### Added
- `project-memory/` with 14 Markdown files: `AI_CONTEXT.md`, `PROJECT.md`, `ARCHITECTURE.md`, `REQUIREMENTS.md`, `CURRENT_STATE.md`, `DECISIONS.md`, `ROADMAP.md`, `TODO.md`, `BUGS.md`, `CHANGELOG.md`, `MEMORY_PROTOCOL.md`, `KNOWLEDGE/research.md`, `KNOWLEDGE/retailers.md`, `KNOWLEDGE/phone-data.md`.
- Twelve decisions recorded in `DECISIONS.md` (D-001 to D-012), taken from the Master Project Instructions and the memory-layer brief.

### Notes
- No repository was available to inspect. Code state was marked `[UNKNOWN]` or `[UNVERIFIED]` throughout. Reconciliation was TODO T-001 (completed 2026-09-26, see above).
- No application code was changed and no dependencies were added.

## Earlier history
`[UNKNOWN]` — no earlier changelog existed. Anything done before 2026-09-21 is not recorded here.
