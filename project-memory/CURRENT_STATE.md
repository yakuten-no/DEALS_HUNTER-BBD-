# BBD HUNTER — Current State

> Purpose: the exact current state of the project. Update after every meaningful implementation change.
> Last updated: 2026-10-01 · Memory layer V0.1

**STATE CONFIDENCE: HIGH for the backend; HIGH for the frontend's automated tests and production build; MEDIUM for the UI as seen in a real browser (not done).** V0.2 was built by an earlier session that had no network, so none of it had ever been run. This session took it over, ran everything for real, found and fixed four defects (see `BUGS.md`), and re-verified. Everything below marked `[VERIFIED]` was actually executed in this session, **in a Linux sandbox** (Ubuntu 24, Python 3.12.3, Node 22.22.2, SQLModel 0.0.47, FastAPI 0.142.2, SQLAlchemy 2.0.54, Pydantic 2.13.5, Vitest 2.1.9, Vite 5.4.21). **It has not been re-run on the owner's Windows PC** — that re-run is the remaining confirmation (T-005). Nothing has been committed or pushed.

Status tags: `[VERIFIED]` confirmed by actually running it · `[BUILT]` written and passed offline static checks but not run live · `[PLANNED]` intended, not built · `[UNKNOWN]` no information.

## Current version
- Project version: **V0.2 (Product & Deal Data Foundation)**, `[VERIFIED]` in a Linux sandbox; Windows re-run pending.
- V0.1 (wishlist, health, dashboard) is included in the same runs and passes — but note V0.1's own test suites **also failed** on current dependency versions before this session's fixes (8 of 18 backend tests from the datetime defect; all frontend suites from the Vitest setup defect). The earlier "V0.1 user-confirmed running" statement should be read as "the app ran for the owner", not "its tests passed on current dependencies".
- Memory layer: V0.1, updated 2026-09-21 → 2026-09-26 → 2026-09-29 → 2026-10-01.

## Test and build results (this session, Linux sandbox)
| Check | Result |
|---|---|
| Baseline before any change (V0.1 only, current deps) | backend 8 failed / 10 passed; frontend 0 tests ran (all suites failed) |
| Baseline with the handed-over V0.2 ZIP (Windows, owner-reported) | backend 67 failed / 32 passed; frontend all 3 suites failed |
| After fixes: `pytest` (backend) | **115 passed, 0 failed** (99 handed over + 16 new regression tests) |
| After fixes: `npm test` (frontend) | **14 passed, 0 failed** (3 suites) |
| After fixes: `npm run build` (`tsc -b && vite build`) | **succeeded** (strict TypeScript check included) |
| Live HTTP check: real `uvicorn` on a throwaway SQLite file, real seed script | health, wishlist create/update/delete, listings, price history, deal assessment (with and without history), 409 on duplicate — all correct; no server tracebacks |
| Frontend TS types vs backend OpenAPI schemas | all 11 checked types match field-for-field |
| Mutation check of the new tests | re-introducing the naive-datetime bug → 81 failures; removing the 409 translation → 10 failures; restored → 115 pass |

## What is working
- **Backend:** V0.1 (health, wishlist CRUD) plus V0.2: Retailer, Product, ProductVariant, RetailerListing, PriceObservation (append-only: no update/delete endpoint), Offer; real foreign keys (`PRAGMA foreign_keys=ON`), uniqueness constraints (duplicates now return a clean **409**), RESTRICT-on-delete-with-dependents (409). Deterministic deal assessment (`GET /api/retailer-listings/{id}/deal-assessment`) and product-name normalization. All timestamps are timezone-aware UTC end to end (D-025).
- **Frontend:** V0.1 dashboard plus the V0.2 Data Explorer tab (Products → Variants → Listings → Price History / Offers / Deal Signals) with honest empty states and a "Demo" badge on fixture rows. Verified by jsdom tests and the production build only — **not yet clicked through in a real browser.**
- **Optional demo seed** (`backend/scripts/seed_demo_data.py`): run against a throwaway database this session; creates clearly-labelled fictional rows (`is_demo=true`, source notes, UI badge); idempotent; never run automatically.

## Partially implemented
- **Wishlist update (PUT)**: backend + hook exist, no UI trigger (unchanged from V0.1).
- **Variant identity (OQ-3)**: RAM/storage/color uniqueness is real; condition, region, warranty are not yet fields.
- **Price-history metrics**: current/lowest/highest/average and previous-price comparison are real; "recent average" and 7/30/90-day lows are not implemented.
- **Deal engine**: assesses one listing at a time, on request; nothing is stored (D-020). **It currently ignores `Offer.valid_from` / `valid_until`, so an expired offer is still counted** — see BUG-006 (open).

## Not implemented
Retailer collectors, the AI layer, notifications, Hunt Mode, WebSocket updates, structured phone specs, browser automation/checkout, automated wishlist-matching (discovery). All expected; none was in V0.2's scope.

## Differences from the V0.2 brief worth knowing (all pre-existing, documented in `DECISIONS.md`)
- `DealAssessment` is a **computed API response, not a database table** (D-020). The brief listed it among the database models; this was a deliberate earlier decision and was left unchanged.
- `Offer` attaches to a `RetailerListing`, not to a specific `PriceObservation`.
- The demo seed script and `is_demo` columns exist (D-022). They are opt-in and labelled, but the brief said not to populate the UI with demo prices; the owner should confirm this is acceptable.

## Current development objective
1. **Re-run on the owner's Windows PC**: `pip install -r requirements.txt` (now requires `sqlmodel>=0.0.47`), `pytest` (expect 115 passing), `npm install`, `npm test` (expect 14), `npm run build`, then click through the Data Explorer (optionally after `python -m scripts.seed_demo_data`). (T-005)
2. Decide on BUG-006 (expired offers counted) — recommended before any further deal-engine work. (T-063)
3. Commit and push V0.2 when satisfied (not done by this session, by instruction). Only then consider V0.3 (`ROADMAP.md`).

## Current blockers
None known. The Windows re-run and a real-browser click-through are the open confirmations.

## Important files
| Path | What it is | Status |
|---|---|---|
| `README.md` (root) | Setup, run, test, seed-data instructions | `[VERIFIED]` commands run here; test counts updated |
| `backend/app/utils.py` | `utcnow()`, `ensure_utc()`, `UTCDatetime` — the datetime convention (D-025) | `[VERIFIED]` |
| `backend/app/services/db_helpers.py` | `commit_unique()` — unique violation → 409 (D-026) | `[VERIFIED]` |
| `backend/app/deal_engine/assessment.py` | The deal engine | `[VERIFIED]` (see BUG-006) |
| `backend/app/models/`, `backend/app/services/`, `backend/app/routers/` | V0.1 wishlist + 6 V0.2 entities | `[VERIFIED]` |
| `backend/tests/test_datetimes.py`, `test_duplicate_conflicts.py` | New regression tests (16) | `[VERIFIED]` |
| `frontend/src/test/setup.ts` | Vitest + jest-dom setup (BUG-002 fix) | `[VERIFIED]` |
| `frontend/src/components/explorer/` | Data Explorer | `[VERIFIED]` tests + build; not browser-tested |
| `project-memory/ARCHITECTURE.md` §12–§13 | Real file trees | current |

## Last meaningful change
2026-10-01 — took over the V0.2 ZIP from the previous session; fixed the timezone-aware datetime defect, the Vitest setup defect, unhandled unique-constraint errors, and a test-helper setup defect; added 16 regression tests; raised the `sqlmodel` minimum to 0.0.47; updated this memory layer and the README's verification note. Not committed.

## How this state was determined (inspection log, 2026-10-01)
1. Cloned the canonical repository (`yakuten-no/DEALS_HUNTER-BBD-`, HEAD `3ca0740` "Implement V0.1 foundation", only V0.1 is on GitHub) and ran V0.1 alone first: 8/18 backend tests and all frontend suites failed on current dependencies — the same two defects the owner later reported for V0.2.
2. Unzipped `BBD-v0_2.zip` over a clean clone; `git diff` against V0.1 showed the real V0.2 changes (19 modified files plus the new models, services, routers, deal engine, tests and explorer components).
3. Read the datetime-bearing code (models, services, deal engine, seed script, conftest) and SQLModel 0.0.47's `UTCDateTime` source to find the root cause rather than patching symptoms.
4. Fixed, re-ran the suites, traced the 5 residual backend failures to two distinct causes (unhandled unique violations; a test helper reusing unique values), fixed those, added regression tests, and mutation-checked them.
5. Ran the real server and seed script end to end; compared frontend types with the backend OpenAPI schema; ran the production build.
6. Not done: a real-browser click-through; a Windows run; any commit or push.
