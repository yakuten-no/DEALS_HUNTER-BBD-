# BBD HUNTER — Current State

> Purpose: the exact current state of the project. Update after every meaningful implementation change.
> Last updated: 2026-09-26 · Memory layer V0.1

**STATE CONFIDENCE: MEDIUM.** This is a real jump from the previous version of this file (2026-09-21, written with no repository at all). The repository now exists and was inspected directly — every status below reflects what's actually in the code, not a guess. What it *can't* yet confirm is runtime behavior: this was built in a sandboxed environment with no network access, so nothing here has been `pip install`-ed, `npm install`-ed, or actually run. See "How this state was determined" at the bottom for exactly what was and wasn't checked, and the root `README.md`'s "A note on how this was verified" section.

Status tags: `[VERIFIED]` confirmed by actually running it · `[BUILT]` written and passed offline static checks (Python: `py_compile`; TypeScript/TSX: parsed with the TypeScript compiler) but not yet run live · `[PLANNED]` intended, not built · `[UNKNOWN]` no information.

## Current version
- Project version: **V0.1**, foundation implementation `[BUILT]` in this session.
- Memory layer: V0.1, first written 2026-09-21, updated 2026-09-26.

## What is working
Nothing is `[VERIFIED]` yet (nothing has been run live). What is `[BUILT]` and, by careful offline review, believed to work:
- Backend: FastAPI app with a real health/database check, full wishlist CRUD (create, list, get, update, delete), request validation (required fields, non-negative budgets, budget_target ≤ budget_max checked on both create and update), 18 pytest tests covering all of it against an isolated in-memory database.
- Frontend: a dashboard that renders the BBD Hunter branding, a natural-language hunt input (with an optional panel for setting exact numeric/boolean constraints by hand), a wishlist panel wired to the real backend (create + list + delete; update exists but has no UI trigger yet — see below), a system-status panel where Backend and Database are genuine live checks and AI/Collectors are honest static "not connected"/"not running" labels, an honest empty-state deal feed (no fabricated products or prices), and a session-only activity log. 8 Vitest tests covering rendering and health-check connected/offline behavior, with the backend mocked.
- Project memory: this file and its siblings, kept in sync with the code as of this update.

## Partially implemented
- **Wishlist update (PUT)**: the backend endpoint and the frontend's `useWishlists().edit()` action both exist and are tested, but no UI control calls it yet (no edit form/button). A person using the dashboard can create and delete entries, not edit one in place.
- **System status**: Backend and Database are live; AI and Collectors are permanently "not connected"/"not running" because neither exists yet — this is correct/honest for V0.1, not a bug, but means those two rows will always read the same regardless of anything the user does, until later phases build the AI layer and collectors.
- **Activity log**: works, but is session-only (React state, not persisted) and only logs a handful of event types wired up in `App.tsx` (backend connect/disconnect, database initialized, wishlist created/removed). It does not yet log a wishlist update, since there's no UI path that triggers one.

## Not implemented
Retailer collectors, price tracking and history, the deal engine (base/guaranteed/conditional/cashback separation, price-history metrics, genuine-drop detection), the AI layer (natural-language parsing into structured preferences, review analysis, discovery), notifications, Hunt Mode, WebSocket live updates (V0.1 polls `/api/health` every 15s instead), and any checkout-related automation. All expected — none of this was in V0.1's scope.

## Current development objective
1. **You (or an AI agent with a network connection) run the Setup steps in the root `README.md` and confirm the app actually installs, starts, connects, and passes its tests.** This is the single most important next step — everything above is offline-reviewed but not yet proven.
2. Fix whatever that first real run surfaces (see `BUGS.md` once anything is found — nothing is recorded there yet because nothing has been run).
3. Then continue V0.2 per `ROADMAP.md` (not started automatically, per this task's instructions).

## Current blockers
- **No network access in the environment this was built in.** Confirmed: both `pip download` and `npm view` failed against their real registries. This is why nothing could be actually executed here — not a code problem, an environment constraint. Resolved by running the Setup steps on a machine with internet access (your Windows PC, or any machine with Python + Node + internet).
- Everything listed under "Not implemented" above is a planned-but-not-yet-blocking gap, not a blocker for V0.1's own goal (a clean, runnable foundation).

## Important files
| Path | What it is | Status |
|---|---|---|
| `README.md` (root) | Setup, run, and test instructions — start here | `[BUILT]` |
| `backend/app/main.py` | FastAPI entry point | `[BUILT]` |
| `backend/app/models/wishlist.py` | Wishlist domain model (table + API schemas) | `[BUILT]` |
| `backend/app/services/wishlist_service.py` | Wishlist business logic, separate from routes | `[BUILT]` |
| `backend/tests/` | 18 pytest tests | `[BUILT]` |
| `frontend/src/App.tsx` | Dashboard layout | `[BUILT]` |
| `frontend/src/hooks/` | `useHealth`, `useWishlists`, `useActivityLog` | `[BUILT]` |
| `frontend/src/App.test.tsx`, `frontend/src/hooks/useHealth.test.ts` | 8 Vitest tests | `[BUILT]` |
| `project-memory/ARCHITECTURE.md` §12 | The actual file tree, in full | `[BUILT]`, current as of this update |

## Last meaningful change
2026-09-26 — built the V0.1 foundation (backend, frontend, tests, docs) and updated this memory layer to match. Previous meaningful change: 2026-09-21, memory layer created with no repository yet.

## How this state was determined (inspection log, 2026-09-26)
Performed in this session, in order:
1. Checked for an existing repository (none found) and confirmed the project-memory written 2026-09-21 had persisted, so it was reused as the starting point rather than recreated from scratch.
2. Tested network access directly (`pip download`, `npm view`): both failed against their real registries. No target Python or Node packages were pre-installed either. This ruled out actually installing dependencies or running the app in this session.
3. Built the full V0.1 scope as files on disk.
4. Ran `python3 -m py_compile` on every backend `.py` file: 0 syntax errors.
5. Parsed every frontend `.ts`/`.tsx` file with the TypeScript compiler's own parser (syntax-only, no module resolution, so no noise from missing `node_modules`): 0 syntax errors across 18 files (the 19th file, `vite-env.d.ts`, is a type-only ambient declaration file with no emittable output, which the parse-based check can't meaningfully evaluate this way — reviewed by hand instead; it's two short interface declarations).
6. Cross-checked that every relative import in the frontend resolves to a real file, that router code calls only service functions that actually exist with matching names, and traced the wishlist validation logic (required fields, budget range on create and on partial update) and the health check by hand against the actual code.
7. Nothing above executed the application or its test suites. That is genuinely unverified until the Setup steps in the root `README.md` are run on a machine with internet access.