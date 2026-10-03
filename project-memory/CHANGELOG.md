# BBD HUNTER — Changelog

> Purpose: meaningful project changes, newest first. Add an entry after every meaningful change (see `MEMORY_PROTOCOL.md`).
> Last updated: 2026-10-01 · Memory layer V0.1

Entry format: `## YYYY-MM-DD — Version or phase — title`, then Added / Changed / Fixed / Removed as needed.

## 2026-10-01 — V0.2 — takeover: made V0.2 actually run (datetime, test setup, 409s)
### Fixed
- **BUG-001** Every database write failed with "Datetime values must have timezone information" on current SQLModel. One convention now everywhere: timezone-aware UTC (D-025). `utcnow()` is aware; new `ensure_utc()` / `UTCDatetime` normalize API input (`observed_at`, `valid_from`, `valid_until`); validation not loosened. The API now emits `Z`-suffixed timestamps.
- **BUG-002** All frontend suites failed with `expect is not defined`. `src/test/setup.ts` now uses `@testing-library/jest-dom/vitest` and explicit `afterEach(cleanup)` (D-027).
- **BUG-003** Duplicate retailer slug / product / variant config / listing URL surfaced as an unhandled database error. Now a clean **409** on create and update (`commit_unique()`, `DuplicateRecordError`, D-026); resolves OQ-10.
- **BUG-004** `tests/test_offers.py::_make_listing` reused unique values; helper now generates distinct ones (assertions untouched).

### Added
- 16 regression tests: `tests/test_datetimes.py` (10: aware `utcnow`, naive/offset normalization, database round-trip, API input and ordering across time zones) and `tests/test_duplicate_conflicts.py` (6). Mutation-checked: reintroducing either bug makes them fail.
- Decisions D-025, D-026, D-027; bugs BUG-001 to BUG-006 recorded (BUG-005 and BUG-006 open).

### Changed
- `backend/requirements.txt`: `sqlmodel>=0.0.47` (the verified version; the datetime convention relies on its `UTCDateTime` type).
- `backend/tests/conftest.py`: the test engine enables `PRAGMA foreign_keys=ON`, matching production.
- `backend/app/main.py`: handler for `DuplicateRecordError` (409). Four services (`retailer`, `product`, `product_variant`, `retailer_listing`) commit through `commit_unique()`.
- README and project-memory updated with the real test counts and verification status.

### Results (Linux sandbox; not yet re-run on Windows)
- Backend `pytest`: **115 passed, 0 failed** (was 67 failed / 32 passed on the owner's Windows run).
- Frontend `npm test`: **14 passed, 0 failed** (was: all 3 suites failing).
- Frontend `npm run build`: **succeeded**.
- Live check with a real `uvicorn` server, the seed script and a throwaway SQLite file: V0.1 and V0.2 endpoints behave correctly; no server errors.

### Notes
- Not committed or pushed, by instruction.
- Open: BUG-006 (deal assessment ignores offer validity windows) and BUG-005 (deprecated constant, harmless). Not fixed here: outside "make V0.2 run".
- V0.3 was not started.

## 2026-09-29 — V0.2 — Product & Deal Data Foundation
### Added
- Backend data model (`backend/app/models/`): `Retailer`, `Product`, `ProductVariant`, `RetailerListing`, `PriceObservation` (append-only -- no update/delete endpoint), `Offer`. Real foreign keys, `PRAGMA foreign_keys=ON` enforcement, uniqueness constraints (retailer slug; product brand+normalized_name; variant product+storage+ram+color; listing URL), and RESTRICT-on-delete-with-dependents (409, never silent data loss) for Product/ProductVariant/RetailerListing.
- `backend/app/normalization.py`: deterministic product-name parsing (brand/RAM/storage/color), matching the V0.2 brief's own worked example exactly.
- `backend/app/deal_engine/`: deterministic deal assessment (`assess_deal()`) -- price-history stats, guaranteed/conditional/cashback totals kept separate, "lowest observed in our history" wording (never "all-time low"), MRP discounts shown only as a caveat never a reason, tri-state (true/false/unknown) signals so "not enough history" is never confused with "checked, and no".
- API endpoints for all six new entities plus `GET /api/retailer-listings/{id}/deal-assessment` (optional `?wishlist_id=`), following V0.1's router/service conventions; shared `NotFoundReferenceError` (422) / `HasDependentsError` (409) exception handlers in `main.py`.
- Frontend Data Explorer (`frontend/src/components/explorer/`): a Products -> Variants -> Listings -> (Price History / Offers / Deal Signals) drill-down, reachable via a new Dashboard/Data Explorer tab in the header. Honest empty states throughout ("No price history available yet.", "No offers available."); a visible "Demo" badge on any `is_demo=true` data.
- `backend/scripts/seed_demo_data.py`: optional, clearly-labelled fixture data (real retailer names as reference data, an always-fictional "Democorp Demo Phone" product, `is_demo=true` throughout) for exercising the Data Explorer during development. Never run automatically.
- 81 new backend tests (99 total: `test_normalization.py`, `test_retailers.py`, `test_products.py`, `test_product_variants.py`, `test_retailer_listings.py`, `test_price_observations.py`, `test_offers.py`, `test_deal_engine.py`) and 6 new frontend tests (14 total: `DataExplorer.test.tsx`, +1 in `App.test.tsx` for the tab switch).
- Seven new architectural decisions, D-018 to D-024 (see `DECISIONS.md`): no SQLModel relationships; `Literal`-at-the-API-layer instead of a mapped `Enum` column; deal assessment computed, not stored; RESTRICT deletes with a friendly check plus a DB-level backstop; the demo-data design; `deal_engine` as a backend subpackage, not a top-level folder; latest-price-per-listing via a single query and Python reduction instead of a SQL window function.

### Changed
- `backend/app/main.py`: registers the six new routers and the two new exception handlers; `app_version` bumped to `0.2.0`.
- `backend/app/database.py`: enables SQLite foreign-key enforcement; `init_db()` now imports all 6 new model modules alongside V0.1's `wishlist`.
- `frontend/src/App.tsx` and `frontend/src/components/layout/Header.tsx`: added the Dashboard/Data Explorer tab switch. All existing V0.1 dashboard content and behavior is unchanged and still the default view.
- `frontend/src/lib/api.ts`: added seven new read functions for the V0.2 endpoints; every V0.1 function is unchanged.
- `README.md`: V0.2 section, expanded API reference, seed-data instructions, updated test counts, updated verification note.
- `collectors/README.md`: now points at the real V0.2 schema and the normalization/deal_engine modules a future collector would feed into.
- `project-memory/ARCHITECTURE.md`: added §13 "Actual layout (V0.2 additions)"; updated the component-status table, data-flow diagram, common-data-model section (now mostly implemented, each entry annotated with where the real thing lives), price/deal-rules section (annotated with what's implemented vs. not), technology-choices table, and open-questions section (OQ-1/OQ-9 fully resolved earlier; OQ-3 partly resolved; OQ-5 more pressing now; new OQ-10).
- `project-memory/CURRENT_STATE.md`, `AI_CONTEXT.md`: fully rewritten for V0.2, same as they were for V0.1's implementation.
- `project-memory/TODO.md`: V0.1's "run it for real" task (T-003) marked done (user-confirmed); added the equivalent V0.2 task (T-005/T-006); added V0.2's own completed-task section; added three new follow-up tasks (T-060 to T-062).
- `project-memory/REQUIREMENTS.md`: V0.2-scoped functional requirements (FR-110 through FR-143 relevant to product/price/offer/normalization) marked with their real implementation status.
- `project-memory/ROADMAP.md`: V0.2 status line updated; V0.3 candidates drafted.

### Notes
- Built in the same kind of sandboxed, no-network environment V0.1 was originally built in -- V0.2 has **not** been run live yet, the same way V0.1 hadn't been at the equivalent point in its own delivery. See `CURRENT_STATE.md` and `README.md`'s verification note for exactly what was and wasn't checked offline.
- No retailer scraping, no AI integration, no checkout automation, and no CAPTCHA/OTP/payment handling was implemented, per this phase's explicit instructions. No new dependencies were added on either side.
- Every V0.1 file was diffed byte-for-byte against its last-known-good copy after this update; all identical except the four files this update deliberately touched (`App.tsx`, `Header.tsx`, `App.test.tsx`, `lib/api.ts`), each confirmed to still satisfy every pre-existing V0.1 test assertion.

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
