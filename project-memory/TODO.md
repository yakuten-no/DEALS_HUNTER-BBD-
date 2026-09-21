# BBD HUNTER — TODO

> Purpose: actionable development tasks by priority and phase. Update when tasks are completed, added, or reprioritized.
> Last updated: 2026-09-21 · Memory layer V0.1

Legend: `[x]` done · `[ ]` open · `[?]` status unknown, verify against the repository first. IDs are permanent; never reuse one.

## P0 — Do first
- [ ] **T-001** Reconcile `project-memory/` with the real repository: inspect it, then correct `CURRENT_STATE.md`, `AI_CONTEXT.md` and `ARCHITECTURE.md` (add an "Actual layout" section).
- [ ] **T-002** Record the real status (done / partial / missing) of each V0.1 item below in `CURRENT_STATE.md`.

## V0.1 — Foundation (status of each item is unknown until T-001)
- [?] **T-010** Repository structure (`frontend/`, `backend/`, `collectors/`, `ai/`, `deal_engine/`, `database/`, `automation/`, `notifications/`, `tests/`, `docs/`; final layout after architectural review)
- [?] **T-011** Backend shell: FastAPI, async, type-hinted
- [?] **T-012** Health/status endpoint
- [?] **T-013** Database shell: SQLite connection and initialization
- [?] **T-014** Basic wishlist model: schema and minimal persistence
- [?] **T-015** Configuration system: environment variables, `.env.example`, no secrets committed
- [?] **T-016** Frontend shell: React, Vite, TypeScript, Tailwind CSS, Framer Motion, Lucide
- [?] **T-017** Premium dashboard UI
- [?] **T-018** Development documentation, including exact Windows install commands
- [ ] **T-019** Basic tests for V0.1 code (health endpoint, wishlist model)

## Memory layer
- [x] **T-030** Create `project-memory/` (2026-09-21)
- [ ] **T-031** Decide whether to store the verbatim Master Project Instructions in the repo (for example under `docs/`). Unknown whether they are already stored.
- [ ] **T-032** Add a pointer that tells every AI session to read `project-memory/AI_CONTEXT.md` first (for example a README section).
- [ ] **T-033** After each phase, re-trim `AI_CONTEXT.md` so it stays short and current.

## Decisions and research to resolve before later phases
- [ ] **T-040** Approve or change the draft roadmap after V0.1 (`ROADMAP.md`).
- [ ] **T-041** Decide the open architectural questions OQ-2 to OQ-9 as each becomes relevant (`ARCHITECTURE.md` section 11). OQ-3 and OQ-4 before V0.2; OQ-7 before any logged-in browser use.
- [ ] **T-042** Research retailer data access, terms and offer presentation before the first collector (RQ-02, RQ-03; `KNOWLEDGE/retailers.md`).
- [ ] **T-043** Find the next Flipkart Big Billion Days dates to set a Hunt Mode target (RQ-01).

## Later phases
Tracked in `ROADMAP.md`. Add concrete tasks here when a phase starts.