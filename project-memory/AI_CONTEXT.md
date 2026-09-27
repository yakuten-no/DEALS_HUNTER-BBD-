# BBD HUNTER — AI Context (read this first)

> Primary handoff file for any AI agent. Keep it short (~120 lines); put detail in the other `project-memory/` files.
> Last updated: 2026-09-26 · Memory layer V0.1

**STATE CONFIDENCE: MEDIUM.** The repository now exists and this file was written from direct inspection of it (not guessed). What's unverified is *runtime behavior*: this was built with no network access, so nothing has actually been installed or run yet. Read `CURRENT_STATE.md` for the full picture before assuming anything below still holds — code changes fast, this file can drift.

Status tags: `[VERIFIED]` confirmed by running it · `[BUILT]` written and passed offline static checks but not run live · `[PLANNED]` intended, not built · `[UNKNOWN]` no information.

## 1. What BBD HUNTER is
A local-first AI shopping-intelligence and deal-hunting app, initially for **smartphones in India**. Goal: "what is the best deal available for MY requirements right now?", not just "did a price drop?" Natural-language requirements → structured preferences → deterministic rules decide anything financial; AI only interprets, classifies, summarizes, discovers, and explains. Never invents prices/discounts/specs; marks uncertainty. Full picture: `PROJECT.md`.

## 2. Current version
- Project: **V0.1**, foundation, `[BUILT]` (not yet run live — see below).
- Memory layer: V0.1, updated 2026-09-26.

## 3. Current objective
1. **Run it for real.** Follow the root `README.md`'s Setup steps on a machine with internet access, confirm it installs/starts/connects, run both test suites. This is the most important next step — see CURRENT_STATE.md for exactly what has and hasn't been checked so far.
2. Fix whatever that surfaces; record real bugs in `BUGS.md`.
3. Continue to V0.2 per `ROADMAP.md` only once V0.1 is confirmed working (not started automatically in this session, per its own instructions).

## 4. Completed work
- `[BUILT]` Backend: FastAPI app, config via environment variables, SQLite + SQLModel, a real (non-hardcoded) health/database check, full wishlist CRUD with validation, 18 pytest tests.
- `[BUILT]` Frontend: React + TS + Vite + Tailwind dashboard — hunt input (natural language, saved as-is, plus an optional manual "exact constraints" panel), wishlist panel (create/list/delete wired to the real backend), live system-status panel (Backend/Database genuinely checked; AI/Collectors honestly static), empty-state deal feed with no fabricated data, session activity log. 8 Vitest tests.
- `[BUILT]` Root `README.md` with full setup/run/test instructions and an honest note on what was and wasn't verifiable in the build environment.
- Full actual file tree: `ARCHITECTURE.md` §12.

## 5. Work in progress
- Wishlist **update** (PUT) works and is tested on the backend, and the frontend hook (`useWishlists().edit()`) exists, but no UI control calls it yet — there's no edit button/form. Create, list, and delete all have working UI.

## 6. Next tasks (full list: `TODO.md`)
1. Run Setup for real (see above) and report/fix anything that breaks.
2. Add a UI trigger for wishlist editing (backend + hook already support it).
3. V0.2 (proposed, needs approval): product/variant/observation/offer schema, price and currency parsing, price-history metrics. See `ROADMAP.md`.

## 7. Important architectural decisions (full text: `DECISIONS.md`)
V0.1-specific (new this session):
- D-013 SQLModel (not bare SQLAlchemy); no migration tool yet (`create_all` only) — deliberate, revisit before real data is at stake.
- D-014 Wishlist `PUT` is a partial update (only sent fields change), not a strict REST replace — documented deviation.
- D-015 Tests live next to their code (`backend/tests/`, colocated in `frontend/src/`), not in a shared root `tests/` (which holds only a README explaining why).
- D-016 Tailwind v3 (not v4), no Framer Motion in V0.1 — conservative choices made with no network access to verify newer tooling.
- D-017 Dashboard palette: warm charcoal + amber accent (a deliberate Bloomberg-Terminal-style reference), with green/rust used *only* as functional price-signal colors — chosen specifically to avoid the generic "near-black + single green/vermilion accent" AI-generated-design cliché.

Carried over from before code existed (still governing): D-001 local-first · D-003 AI interprets, rules decide · D-004 isolated retailer adapters · D-005 never invent data, mark uncertainty · D-006 separate price components · D-007 never compare non-equivalent variants · D-008 no CAPTCHA/anti-bot bypass, no stored secrets, human-controlled checkout · D-011 vendor-independent Markdown memory.

## 8. Known bugs and blockers
- `BUGS.md`: empty. Nothing has been run live yet, so this means "not yet tested," not "confirmed bug-free."
- Blocker: no network access in the build environment — resolved by running Setup on a machine with internet. See `CURRENT_STATE.md` for the full inspection log of what *was* checked offline (Python syntax via `py_compile`: clean; TypeScript/TSX syntax via the TS compiler's parser: clean across 18 files; every import cross-checked to resolve).

## 9. Important files and directories
- Start here: root `README.md` (setup/run/test), then this file, then `CURRENT_STATE.md`.
- `ARCHITECTURE.md` §12 has the full real file tree with a one-line purpose for every file.
- `backend/app/` (FastAPI), `frontend/src/` (React dashboard), `backend/tests/` + `frontend/src/**/*.test.ts(x)` (tests).
- `collectors/`, `ai/`, `automation/` each exist with only a README explaining their future purpose — empty on purpose, not forgotten.
- `database/bbd_hunter.db` is created automatically at runtime; gitignored.

## 10. Technology stack (as actually built; see D-002, D-013, D-016)
Frontend: React 18, Vite, TypeScript, Tailwind CSS v3, Lucide icons (no Framer Motion in V0.1). Backend: Python, FastAPI, SQLModel, asyncio-capable (Uvicorn). Database: SQLite, no migrations yet. Realtime: polling (`/api/health` every 15s) — WebSockets still `[PLANNED]`. AI: not wired in yet — `ai/` is an empty placeholder.

## 11. Constraints
Same as before code existed, now enforced in code where applicable: never invent prices/discounts/specs/availability/offers (the deal feed shows an honest empty state, not fake products); never request/store passwords/PINs/CVVs/OTPs/secrets (nothing of the sort exists in V0.1); no CAPTCHA bypass or anti-bot circumvention; no paid AI API dependency; build incrementally and preserve working functionality; complete files, exact install commands, explain decisions in plain language (user is beginner/intermediate); TypeScript types and Python type hints throughout; tests for major components; memory stays vendor-independent with no secrets or large code copies (see `MEMORY_PROTOCOL.md`).

## 12. Last updated
2026-09-26, by an AI agent, from direct inspection of the repository built in this session.
