# BBD HUNTER — TODO

> Purpose: actionable development tasks by priority and phase. Update when tasks are completed, added, or reprioritized.
> Last updated: 2026-09-26 · Memory layer V0.1

Legend: `[x]` done · `[ ]` open · `[?]` status unknown, verify against the repository first. IDs are permanent; never reuse one.

## P0 — Do first
- [x] **T-001** Reconcile `project-memory/` with the real repository. Done 2026-09-26 — `CURRENT_STATE.md`, `AI_CONTEXT.md`, `ARCHITECTURE.md` (added §12 "Actual layout"), `DECISIONS.md`, `REQUIREMENTS.md`, `CHANGELOG.md`, `ROADMAP.md` all updated from direct inspection.
- [x] **T-002** Record the real status of each V0.1 item in `CURRENT_STATE.md`. Done 2026-09-26.
- [ ] **T-003** Run the app for real: follow the root `README.md` Setup steps on a machine with internet access (this was built in a sandbox with no network — see `CURRENT_STATE.md`). Confirm `pip install` / `npm install` succeed, the backend starts and its health check reports "connected", the frontend loads and shows the backend as Connected, and both test suites (`pytest`, `npm test`) pass. This is the most important open task — everything else in V0.1 is offline-reviewed but not yet proven to actually run.
- [ ] **T-004** Fix whatever T-003 surfaces. Record genuine bugs found in `BUGS.md` as they're found (none are recorded yet, precisely because nothing has been run live).

## V0.1 — Foundation
- [x] **T-010** Repository structure — built as: `frontend/`, `backend/`, `collectors/` (README only), `ai/` (README only), `database/` (README only), `automation/` (README only), `tests/` (README only, explains the split), `project-memory/`. No `deal_engine/`, `notifications/`, or `docs/` yet — see `ARCHITECTURE.md` §3 note and §12 for the real tree.
- [x] **T-011** Backend shell: FastAPI, type-hinted, async-capable (Uvicorn) — `[BUILT]`, not yet run live.
- [x] **T-012** Health/status endpoint — `[BUILT]`; a real DB check via `SELECT 1`, not hardcoded.
- [x] **T-013** Database shell: SQLite connection and initialization (`init_db()` on startup) — `[BUILT]`.
- [x] **T-014** Basic wishlist model: schema and full CRUD persistence (more than "minimal") — `[BUILT]`.
- [x] **T-015** Configuration system: environment variables via pydantic-settings, `backend/.env.example` and `frontend/.env.example`, no secrets committed — `[BUILT]`.
- [x] **T-016** Frontend shell: React, Vite, TypeScript, Tailwind CSS, Lucide — `[BUILT]`. Framer Motion deliberately **not** included in V0.1 (D-016 in `DECISIONS.md`); add it later if real animation needs outgrow CSS transitions.
- [x] **T-017** Premium dashboard UI — `[BUILT]`: hunt input, wishlist panel, live system status, honest empty deal feed, activity log. Design reasoning in D-017.
- [x] **T-018** Development documentation, including exact setup commands (Windows and macOS/Linux both given) — `[BUILT]`, root `README.md`.
- [x] **T-019** Tests: 18 backend (pytest) + 8 frontend (Vitest) — `[BUILT]`, not yet run live (T-003 covers actually running them).

## New from this session
- [ ] **T-020** Wire up a UI control for wishlist **update** — the backend `PUT` endpoint and the frontend `useWishlists().edit()` action both exist and are tested, but no button/form calls it yet. See `CURRENT_STATE.md`, "Partially implemented."

## Memory layer
- [x] **T-030** Create `project-memory/` (2026-09-21).
- [ ] **T-031** Decide whether to store the verbatim Master Project Instructions in the repo. Still open — not stored anywhere in `BBD/` as of this update.
- [x] **T-032** Add a pointer that tells every AI session to read `project-memory/AI_CONTEXT.md` first. Done 2026-09-26 — see the "Project memory" section of the root `README.md`.
- [ ] **T-033** After each phase, re-trim `AI_CONTEXT.md` so it stays short and current. (Kept to ~110 lines in this update; keep checking as content grows.)

## Decisions and research to resolve before later phases
- [ ] **T-040** Approve or change the draft roadmap after V0.1 (`ROADMAP.md`).
- [ ] **T-041** Decide the still-open architectural questions as each becomes relevant (`ARCHITECTURE.md` §11): OQ-2, OQ-3, OQ-4, OQ-6, OQ-7, OQ-8. (OQ-1, OQ-5, OQ-9 are now resolved or deliberately deferred — see §11.) OQ-3 and OQ-4 before V0.2; OQ-7 before any logged-in browser use.
- [ ] **T-042** Research retailer data access, terms and offer presentation before the first collector (RQ-02, RQ-03; `KNOWLEDGE/retailers.md`).
- [ ] **T-043** Find the next Flipkart Big Billion Days dates to set a Hunt Mode target (RQ-01).
- [ ] **T-044** Introduce a real migration tool (e.g. Alembic) before the database holds data worth preserving across a schema change (OQ-5, D-013).

## Later phases
Tracked in `ROADMAP.md`. Add concrete tasks here when a phase starts.

