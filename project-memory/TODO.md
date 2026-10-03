# BBD HUNTER — TODO

> Purpose: actionable development tasks by priority and phase. Update when tasks are completed, added, or reprioritized.
> Last updated: 2026-10-01 · Memory layer V0.1

Legend: `[x]` done · `[ ]` open · `[?]` status unknown, verify against the repository first. IDs are permanent; never reuse one.

## P0 — Do first
- [x] **T-001** Reconcile `project-memory/` with the real repository. Done 2026-09-26, redone for V0.2 on 2026-09-29 (this update's own "CRITICAL FIRST STEP").
- [x] **T-002** Record the real status of each V0.1 item in `CURRENT_STATE.md`. Done 2026-09-26.
- [x] **T-003** Run V0.1 for real. **Done** — the user reported V0.1 "already implemented and running locally" at the start of the V0.2 session (2026-09-29). V0.2 is a new, separate "run it for real" task — see T-005.
- [x] **T-004** Fix whatever T-003 surfaces. No bugs were reported alongside the "running locally" confirmation, so `BUGS.md` stays empty for V0.1. If something surfaces later, record it there.
- [ ] **T-005** Re-run V0.2 on the owner's Windows PC (partly done). **Done 2026-10-01 in a Linux sandbox:** `pytest` 115 passed, `npm test` 14 passed, `npm run build` succeeded, live server + seed script checked. **Still open:** on Windows, run `pip install -r requirements.txt` (needs `sqlmodel>=0.0.47`), `pytest` (expect 115), `npm install`, `npm test` (expect 14), `npm run build`, then click through the Data Explorer in a real browser (optionally after `python -m scripts.seed_demo_data`).
- [x] **T-006** Fix whatever T-005 surfaces. Done 2026-10-01 for everything surfaced so far: BUG-001 to BUG-004 resolved (see `BUGS.md`). Anything the Windows re-run finds goes in `BUGS.md`.

## V0.1 — Foundation (all done; kept here as the historical record)
- [x] **T-010** through **T-019** — repository structure, backend shell, health endpoint, database shell, wishlist model, configuration, frontend shell, dashboard UI, documentation, tests. All `[BUILT]`; V0.1 as a whole is now `[VERIFIED]` (T-003). Detail unchanged from the previous update — see `CHANGELOG.md`'s V0.1 entries.

## V0.2 — Product & Deal Data Foundation (this session)
- [x] **T-050** Core domain model: Retailer, Product, ProductVariant, RetailerListing, PriceObservation, Offer — real foreign keys, uniqueness constraints, RESTRICT-on-delete-with-dependents. `[BUILT]`.
- [x] **T-051** Deterministic deal assessment (`backend/app/deal_engine/`) covering the six named scenarios (under/over budget, price drop, no history, conditional offer, unavailable listing). `[BUILT]`.
- [x] **T-052** Deterministic product-name normalization (`backend/app/normalization.py`), matching the brief's own worked example. `[BUILT]`.
- [x] **T-053** API endpoints for all six new entities plus the deal-assessment view, following V0.1's router/service conventions. `[BUILT]`.
- [x] **T-054** Frontend Data Explorer: Products → Variants → Listings → History/Offers/Deal Signals, with honest empty states and demo-data badging. `[BUILT]`.
- [x] **T-055** Optional, clearly-labelled demo/fixture seed script, never run automatically. `[BUILT]`.
- [x] **T-056** Tests: 81 new backend (database/model behavior, normalization, all six deal-engine scenarios, representative API validation) + 6 new frontend. All existing V0.1 tests preserved and confirmed unchanged (byte-diffed). `[BUILT]`.
- [x] **T-057** Update `project-memory/` (this file plus `CURRENT_STATE.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `CHANGELOG.md`, `AI_CONTEXT.md`, `REQUIREMENTS.md`, `ROADMAP.md`). Done.

## Carried over from V0.1
- [ ] **T-020** Wire up a UI control for wishlist **update** — the backend `PUT` endpoint and the frontend `useWishlists().edit()` action both exist and are tested, but no button/form calls it yet. See `CURRENT_STATE.md`, "Partially implemented."

## New from this session
- [x] **T-060** OQ-10 decided and done 2026-10-01: unique-constraint violations return a clean 409 (D-026, BUG-003).
- [ ] **T-061** Finish OQ-3 (variant identity): add condition (new/refurbished/open-box), region, and warranty to `ProductVariant`, per the original proposal in `ARCHITECTURE.md` §5. RAM/storage/color is already done.
- [ ] **T-062** Decide how (or whether) a `Wishlist` entry should get linked to a specific `Product`/`ProductVariant` it's shopping for, rather than the deal-assessment endpoint taking an ad hoc `wishlist_id` per request. Needed before automated "does this match my wishlist" scanning (discovery) can exist.

- [ ] **T-063** Fix BUG-006: make the deal engine ignore offers that are expired or not yet active (`valid_from` / `valid_until`), add a caveat saying how many were ignored, and add tests (expired, not-yet-active, open-ended). Recommended before any further deal-engine work.
- [ ] **T-064** Commit and push the verified V0.2 (deliberately not done by the takeover session). Suggested order: review `git diff`, commit, push.
- [ ] **T-065** Owner to confirm the demo seed script / `is_demo` design (D-022) is acceptable given the brief's "no demo prices to populate the UI" rule, or remove it.
- [ ] **T-066** Fix BUG-005 (deprecated `HTTP_422_UNPROCESSABLE_ENTITY` in the V0.1 wishlist router) — low priority.

## Memory layer
- [x] **T-030** Create `project-memory/` (2026-09-21).
- [ ] **T-031** Decide whether to store the verbatim Master Project Instructions in the repo. Still open.
- [x] **T-032** Add a pointer that tells every AI session to read `project-memory/AI_CONTEXT.md` first. Done — root `README.md`'s "Project memory" section.
- [ ] **T-033** After each phase, re-trim `AI_CONTEXT.md` so it stays short and current. (Kept to ~120 lines in this update; keep checking as content grows.)

## Decisions and research to resolve before later phases
- [ ] **T-040** Approve or change the draft roadmap after V0.2 (`ROADMAP.md`).
- [ ] **T-041** Decide the still-open architectural questions as each becomes relevant (`ARCHITECTURE.md` §11): OQ-2, OQ-4, OQ-6, OQ-7, OQ-8, OQ-10 (new). OQ-3 is now partly resolved (see T-061); OQ-1, OQ-5, OQ-9 are resolved or deliberately deferred.
- [ ] **T-042** Research retailer data access, terms and offer presentation before the first collector (RQ-02, RQ-03; `KNOWLEDGE/retailers.md`). More concrete now that `collectors/README.md` points at the real schema to target.
- [ ] **T-043** Find the next Flipkart Big Billion Days dates to set a Hunt Mode target (RQ-01).
- [ ] **T-044** Introduce a real migration tool (e.g. Alembic) before the database holds data worth preserving across a schema change (OQ-5, D-013). More pressing now than at V0.1 — there's real price-history/offer data at stake once this app is in real use.

## Later phases
Tracked in `ROADMAP.md`. Add concrete tasks here when a phase starts.

