# BBD HUNTER — Bugs and Technical Issues

> Purpose: known bugs and technical issues. Add an entry when you find one and update its status when it changes. Do not delete resolved entries; mark them Resolved.
> Last updated: 2026-10-01 · Memory layer V0.1

## Open

### BUG-006 — Deal assessment counts offers that are expired or not yet active
- **Issue**: `assess_deal()` (`backend/app/deal_engine/assessment.py`) sums every offer attached to a listing and never consults `Offer.valid_from` / `Offer.valid_until`. An expired guaranteed offer still lowers `effective_price_guaranteed`; an expired conditional offer still raises `potential_effective_price`'s discount.
- **Severity**: High (a misleading price shown with unwarranted certainty; conflicts with D-005/D-006 and the V0.2 brief's "active offers").
- **Reproduction**: create a listing with one price observation and a guaranteed ₹1000 offer whose `valid_until` is in the past; `GET /api/retailer-listings/{id}/deal-assessment` still applies the ₹1000. (Found by reading the code this session; not yet covered by a test.)
- **Status**: Open — deliberately not changed in the takeover session, whose scope was "make V0.2 run", not new deal logic.
- **Suspected cause**: validity window stored but never used by the engine.
- **Solution**: proposed — filter offers to those active at assessment time and add a caveat stating how many were ignored; add tests for expired, not-yet-active, and open-ended offers. (T-063)
- **Found**: 2026-10-01, V0.2
- **Related**: `assessment.py`, `models/offer.py`, D-005, D-006

### BUG-005 — Deprecated HTTP 422 constant in the V0.1 wishlist router
- **Issue**: `backend/app/routers/wishlists.py` uses `status.HTTP_422_UNPROCESSABLE_ENTITY`, which current Starlette marks deprecated; pytest shows a deprecation warning. Behaviour is correct.
- **Severity**: Low
- **Status**: Open (harmless today; would matter only if a future Starlette removes the name). Fix: use the literal `422` or `HTTP_422_UNPROCESSABLE_CONTENT`.
- **Found**: 2026-10-01, V0.1
- **Related**: `backend/app/routers/wishlists.py`

## Resolved

### BUG-001 — Every database write failed: naive datetimes rejected by SQLModel
- **Issue**: `ValueError: Datetime values must have timezone information.` on every insert into any table with a `datetime` column (wishlists, and all six V0.2 entities).
- **Severity**: High (core feature broken; 67 of 99 backend tests failed on the owner's Windows run; 8 of 18 even for V0.1 alone).
- **Reproduction**: `pip install -r backend/requirements.txt` (current SQLModel; verified on 0.0.47), then `pytest` in `backend/`.
- **Status**: Resolved 2026-10-01.
- **Suspected cause (confirmed)**: SQLModel maps `datetime` fields to `UTCDateTime`, which refuses naive values on write and returns aware UTC on read. The project's `utcnow()` deliberately returned naive UTC (a V0.1 convention written without being able to run it).
- **Solution**: one convention everywhere — timezone-aware UTC (D-025). `utcnow()` now returns an aware datetime; new `ensure_utc()` and `UTCDatetime` normalize API input (`observed_at`, `valid_from`, `valid_until`; naive input is interpreted as UTC, offsets are converted). Validation was not loosened. `requirements.txt` now requires `sqlmodel>=0.0.47`. Side benefit: the API now emits `...Z` timestamps, so browsers no longer misread them as local time.
- **Found**: 2026-10-01 (reported by owner for V0.2; reproduced for V0.1), V0.1/V0.2
- **Related**: `backend/app/utils.py`, `models/price_observation.py`, `models/offer.py`, `tests/test_datetimes.py` (10 tests), D-025

### BUG-002 — All frontend test suites failed: `expect is not defined`
- **Issue**: every Vitest suite failed at load from `src/test/setup.ts` (`@testing-library/jest-dom`).
- **Severity**: High (no frontend test could run).
- **Status**: Resolved 2026-10-01.
- **Suspected cause (confirmed)**: the default jest-dom entry point calls a *global* `expect`; Vitest `globals` is off (tests import from `vitest`). With globals off, Testing Library's automatic per-test cleanup also never registers.
- **Solution**: `import "@testing-library/jest-dom/vitest"` plus an explicit `afterEach(cleanup)` in `setup.ts`. Verified necessary: removing the cleanup makes 7 tests fail with duplicate-element errors. No test was altered, removed, or weakened.
- **Found**: 2026-10-01 (owner-reported), V0.1/V0.2
- **Related**: `frontend/src/test/setup.ts`, D-027

### BUG-003 — Duplicate unique values crashed with an unhandled database error (HTTP 500)
- **Issue**: creating or updating a retailer with an existing slug, a product with an existing brand+normalized name, a variant with an existing storage/RAM/colour, or a listing with an existing URL raised a raw `IntegrityError`. Under FastAPI's `TestClient` this is re-raised into the test; in production it is a 500.
- **Severity**: Medium (data stayed intact; response quality and test failures).
- **Status**: Resolved 2026-10-01.
- **Suspected cause (confirmed)**: no translation of unique violations; earlier tests only asserted `status_code >= 400`, which never ran.
- **Solution**: `commit_unique()` (`services/db_helpers.py`) rolls back and raises `DuplicateRecordError` only for genuine unique violations (other integrity errors still propagate); `main.py` maps it to **409**. Covers create and update paths. Resolves OQ-10. (D-026)
- **Found**: 2026-10-01, V0.2
- **Related**: `tests/test_duplicate_conflicts.py` (6 tests), D-026

### BUG-004 — Test helper created duplicate unique rows
- **Issue**: `tests/test_offers.py::_make_listing` used the same product name, retailer slug and listing URL on every call, so `test_list_offers_scoped_to_listing` (which calls it twice) violated the app's own uniqueness rules during setup.
- **Severity**: Low (test-only).
- **Status**: Resolved 2026-10-01. Only the helper changed (per-call counter for unique values); every assertion is untouched.
- **Found**: 2026-10-01, V0.2
- **Related**: `backend/tests/test_offers.py`

## Severity scale
- **Critical**: data loss; security or secrets exposure; an action taken on wrong financial information.
- **High**: a wrong or misleading price, discount, spec or availability shown (or shown with unwarranted certainty); a core feature broken.
- **Medium**: a feature works incorrectly but has a workaround; performance problems that hurt sale-event use.
- **Low**: cosmetic or minor.

## Entry template
```
### BUG-### — short title
- **Issue**: what is wrong
- **Severity**: Critical / High / Medium / Low
- **Reproduction**: steps, or [UNKNOWN]
- **Status**: Open / In progress / Resolved (date) / Won't fix (reason)
- **Suspected cause**: or [UNKNOWN]
- **Solution**: what fixed it, or [UNKNOWN]
- **Found**: YYYY-MM-DD, version
- **Related**: files, tests, decisions
```
