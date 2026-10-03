# BBD HUNTER — AI Context (read this first)

> Primary handoff file for any AI agent. Keep it short (~120 lines); put detail in the other `project-memory/` files.
> Last updated: 2026-10-01 · Memory layer V0.1

**STATE CONFIDENCE: HIGH (backend, frontend tests/build); MEDIUM (UI in a real browser — not done).** V0.2 was handed over built-but-never-run; on 2026-10-01 it was run for real, four defects were fixed, and it now passes: backend `pytest` **115 passed**, frontend `npm test` **14 passed**, `npm run build` **succeeded**, plus a live-server check. That was a **Linux sandbox**, not the owner's Windows PC; the Windows re-run is still open (T-005). Nothing is committed or pushed. Read `CURRENT_STATE.md` before assuming anything below still holds.

Status tags: `[VERIFIED]` confirmed by running it · `[BUILT]` written and passed offline static checks but not run live · `[PLANNED]` intended, not built · `[UNKNOWN]` no information.

## 1. What BBD HUNTER is
A local-first AI shopping-intelligence and deal-hunting app, initially for **smartphones in India**. Goal: "what is the best deal available for MY requirements right now?", not just "did a price drop?" AI only interprets/explains; deterministic rules and the deal engine decide anything with financial meaning. Never invents prices/discounts/specs; marks uncertainty. Full picture: `PROJECT.md`.

## 2. Current version
- Project: **V0.2 (Product & Deal Data Foundation)**, `[VERIFIED]` (Linux sandbox; Windows re-run pending), on **V0.1**.
- Memory layer: V0.1, updated through 2026-10-01.

## 3. Current objective
1. **Re-run on the owner's Windows PC**: `pip install -r requirements.txt` (needs `sqlmodel>=0.0.47`), `pytest` (expect 115), `npm install`, `npm test` (expect 14), `npm run build`, click through the Data Explorer (optionally `python -m scripts.seed_demo_data` first). (T-005)
2. Fix BUG-006 — the deal engine ignores offer validity windows, so expired offers are counted (T-063).
3. Owner commits and pushes (not done by any session so far). Only then consider V0.3 (`ROADMAP.md`).

## 4. Completed work
- `[VERIFIED]` V0.1: health/status, full wishlist CRUD, the dashboard (its tests had also been failing on current dependencies until 2026-10-01; fixed).
- `[VERIFIED]` V0.2 backend: `Retailer`, `Product`, `ProductVariant`, `RetailerListing`, `PriceObservation` (append-only), `Offer` — real FKs, uniqueness constraints, RESTRICT-on-delete-with-dependents (409, never silent data loss). Deterministic deal assessment (`app/deal_engine/`) and product-name normalization (`app/normalization.py`). Duplicates return 409. All timestamps are timezone-aware UTC. 115 backend tests (18 V0.1 + 81 V0.2 + 16 regression).
- `[VERIFIED]` (jsdom tests + build; not browser-tested) V0.2 frontend: a Data Explorer tab (Products → Variants → Listings → History/Offers/Deal Signals), honest empty states throughout, visible "Demo" badges on fixture data. 14 frontend tests (8 + 6).
- `[VERIFIED]` An optional, clearly-labelled demo-data seed script (`backend/scripts/seed_demo_data.py`) — never run automatically.
- Full actual file tree: `ARCHITECTURE.md` §12 (V0.1) + §13 (V0.2 additions).

## 5. Work in progress
- Wishlist update (PUT) still has no UI trigger (unchanged from V0.1).
- Variant identity (OQ-3) is half-built: RAM/storage/color is real; condition/region/warranty are not yet fields.
- The deal engine assesses one listing at a time on request — it doesn't yet scan for deals matching a wishlist unprompted (discovery is still future work).
- BUG-006 (open, High): the engine counts offers regardless of `valid_from`/`valid_until`.
- `DealAssessment` is a computed response, not a table (D-020) — differs from the V0.2 brief's wording; unchanged.

## 6. Next tasks (full list: `TODO.md`)
1. Windows re-run (T-005), then BUG-006 (T-063), then commit/push (T-064).
2. V0.3 candidates (proposed, needs approval): the first retailer collector (needs OQ-2, OQ-7 decided first), or the AI layer for natural-language → structured preferences (needs the provider abstraction), or wishlist-to-product matching (needs OQ-3 finished). See `ROADMAP.md`.

## 7. Important architectural decisions (full text: `DECISIONS.md`)
V0.2-specific (D-018 to D-024), plus takeover-session decisions (D-025 to D-027):
- D-018 No SQLModel `Relationship()` anywhere — plain FKs + explicit `select()` queries, for the same "can't verify by running it" reason V0.1 avoided validators on table classes.
- D-019 `availability`/`offer_type` are plain `str` columns; `Literal` validation lives only at the API layer (sidesteps a real SQLAlchemy Enum name-vs-value ambiguity).
- D-020 Deal assessment is computed on request, never stored.
- D-021 Deletes with dependents are RESTRICTed (409) — an explicit friendly check plus `PRAGMA foreign_keys=ON` as a backstop.
- D-022 Demo data: real retailer names (reference data only) + an always-fictional product + a real `is_demo` DB column + visible frontend badging.
- D-023 `deal_engine` lives inside `backend/app/`, not as a top-level sibling folder.
- D-024 Latest-price-per-listing uses one query + a Python reduction, not a SQL window function (SQLite version uncertainty).
- D-025 **All timestamps are timezone-aware UTC** (`utcnow()`, `ensure_utc()`, `UTCDatetime`); naive API input means UTC. Supersedes V0.1's naive-UTC convention.
- D-026 Unique-constraint violations → clean HTTP **409** via `commit_unique()` (resolves OQ-10).
- D-027 Test infra mirrors production: Vitest uses `jest-dom/vitest` + explicit cleanup; backend test engine enables `PRAGMA foreign_keys=ON`.

Carried over from V0.1 (still governing): D-001 local-first · D-003 AI interprets, rules decide · D-004 isolated retailer adapters · D-005 never invent data, mark uncertainty, "lowest observed in our history" never "all-time low" · D-006 separate guaranteed/conditional/cashback · D-007 never compare non-equivalent variants · D-008 no CAPTCHA/anti-bot bypass, no stored secrets · D-013 SQLModel, no migrations yet · D-016 Tailwind v3, no Framer Motion.

## 8. Known bugs and blockers
- `BUGS.md`: BUG-001 to BUG-004 **resolved** 2026-10-01 (naive datetimes; Vitest setup; unhandled duplicates; test-helper reuse). **Open:** BUG-006 (expired offers counted — High) and BUG-005 (deprecated constant — Low).
- No blockers. Open confirmations: Windows re-run; real-browser click-through of the Data Explorer.
- Owner to confirm the demo seed design (D-022 / T-065) is acceptable.

## 9. Important files and directories
- Start here: root `README.md`, then this file, then `CURRENT_STATE.md`.
- `ARCHITECTURE.md` §12+§13 have the complete real file tree with a one-line purpose per file.
- `backend/app/utils.py` (datetime convention), `backend/app/services/db_helpers.py` (409s), `backend/app/deal_engine/`, `backend/app/normalization.py`, `backend/app/models/` (6 new entities + V0.1's Wishlist), `backend/scripts/seed_demo_data.py`.
- `frontend/src/components/explorer/` (the Data Explorer), `frontend/src/hooks/useExplorerData.ts`.
- `collectors/`, `ai/`, `automation/` still each just a README — empty on purpose; `collectors/README.md` now points at the real schema to target.

## 10. Technology stack (as actually built; see D-002, D-013, D-016, D-018, D-019)
Unchanged from V0.1: React 18, Vite, TypeScript, Tailwind v3, Lucide (no Framer Motion). Python, FastAPI, SQLModel, Uvicorn. SQLite, no migrations. Polling, not WebSockets. No AI wired in yet. V0.2 added no new dependencies on either side; the backend now requires `sqlmodel>=0.0.47`.

## 11. Constraints
Same as V0.1, now enforced across more of the app: never invent prices/discounts/specs/availability/offers (V0.2's empty states — "No price history available yet.", "No offers available." — and demo-data labelling both enforce this in code, not just policy); never "all-time low", only "lowest observed in our history" once there's enough history to say so (tested); guaranteed/conditional/cashback always kept separate (tested); RESTRICT, never CASCADE, on deletes that would lose price history; no CAPTCHA bypass, no stored secrets; no paid AI API; preserve working functionality (all V0.1 tests still pass); use timezone-aware UTC datetimes only; complete files, exact commands, plain-language explanations; TypeScript types and Python type hints throughout; tests for major components; memory stays vendor-independent (see `MEMORY_PROTOCOL.md`).

## 12. Last updated
2026-10-01, by an AI agent that took over the V0.2 ZIP, ran it for real, fixed what broke, and verified by execution (Linux sandbox).
