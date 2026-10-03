# BBD HUNTER — Architecture

> Purpose: the system architecture — components, data flow, interfaces, boundaries, technology choices.
> Last updated: 2026-10-01 · Memory layer V0.1 · Project version: V0.2 (Product & Deal Data Foundation) — V0.2 verified by execution on 2026-10-01 (Linux sandbox; Windows re-run pending) — see CURRENT_STATE.md

**STATUS: mixed.** Sections 12 and 13 describe what was actually built (V0.1 and V0.2 respectively) and are `[BUILT]` (written, passed offline static checks — syntax, cross-file references, field-name cross-checks — but V0.2 is not yet confirmed by actually running it; V0.1 has since been confirmed working by the user). Everything else in this file is either still-intended architecture from the Master Project Instructions (marked *[source: Master]*), a labelled *[architect note]* or *[draft]*, or explicitly resolved/updated where noted. This file, CURRENT_STATE.md, DECISIONS.md, and TODO.md were updated from direct inspection of the repository built in this and the previous session, not guessed — both this V0.2 update's "CRITICAL FIRST STEP" and V0.1's T-001 required this.

## 1. Principles
1. Modular: collectors, AI, deal engine, database, automation and notifications are separate components. *[source: Master]*
2. Deterministic core: prices, constraints and deal decisions come from rules and stored data, never from free-form LLM reasoning (D-003).
3. Honest data: derived values carry provenance and uncertainty; unknown is not the same as false (D-005).
4. Local-first: everything runs on one Windows PC; external services are optional (D-001).
5. Isolated retailer code: no other component may depend on a retailer's HTML (D-004).
6. Incremental: build the smallest working version, test it, then extend (D-010).

## 2. Data flow

### A. Requirement to decision (interpretation pipeline) *[source: Master]*
```
USER (natural language)
  -> AI INTERPRETATION            (untrusted output)
  -> STRUCTURED PREFERENCES       (schema-validated)
  -> DETERMINISTIC RULE ENGINE    (max price, min storage, required variant, availability, seller conditions)
  -> DEAL ENGINE                  (price components, history context)
  -> AUTOMATION                   (alerts; later, browser-assisted checkout with human confirmation)
```

### B. Data to alerts (collection pipeline) *[draft, derived from Master]*
```
Retailer sites
  -> COLLECTOR ADAPTER (one per retailer)
  -> COMMON PRODUCT / OBSERVATION SCHEMA
  -> NORMALIZATION (model / variant / seller / condition matching)
  -> DATABASE (SQLite: products, variants, listings, observations, offers, wishlist, events)
  -> PRICE-HISTORY METRICS + DEAL ENGINE
  -> EVENTS
  -> WEBSOCKET -> DASHBOARD (Normal / Hunt Mode)   and   NOTIFICATIONS
```
**V0.2 actual, for the middle of this pipeline** (the parts that don't need a live collector to exist and test): the "COMMON PRODUCT / OBSERVATION SCHEMA" is now real (`backend/app/models/` — Retailer, Product, ProductVariant, RetailerListing, PriceObservation, Offer; section 13). "NORMALIZATION" is now real but deliberately basic (`backend/app/normalization.py` — deterministic pattern matching, not fuzzy/semantic matching; see its own docstring and OQ-3). "PRICE-HISTORY METRICS + DEAL ENGINE" is now real (`backend/app/deal_engine/` — computed on request, not stored; D-020). "COLLECTOR ADAPTER", "DATABASE... events", "EVENTS", "WEBSOCKET", and "NOTIFICATIONS" are all still `[PLANNED]`, not touched in V0.2.

## 3. Components

| Component | Responsibility | Actual/intended location | Status |
|---|---|---|---|
| Frontend | Dashboard: hunt input, wishlist, live system status, honest empty deal feed, session activity log, **+ V0.2: Data Explorer** (products -> variants -> listings -> history/offers/deal signals) | `frontend/` | `[BUILT]` (no Hunt Mode UI yet, no live product data — V0.2's data is manual/demo-seeded only) |
| Backend API | HTTP API, config, health/status, wishlist CRUD, **+ V0.2: product/retailer/listing/observation/offer CRUD, deal-assessment endpoint** | `backend/` | `[BUILT]` (REST only; no WebSocket yet) |
| Database | SQLite persistence — wishlist table, **+ V0.2: retailers, products, product_variants, retailer_listings, price_observations, offers, with real foreign keys and uniqueness constraints** | `database/` | `[BUILT]` (no migrations yet — see D-013, D-024) |
| Normalization | Deterministic product-name parsing (brand/RAM/storage/color) | `backend/app/normalization.py` | `[BUILT]` in V0.2 (basic, pattern-matching only — see OQ-3) |
| Deal engine | Price components, history metrics, transparent deal signals | `backend/app/deal_engine/` | `[BUILT]` in V0.2 as a computed service (D-020, D-023); the deterministic *rule engine* for wishlist constraints (max price, min storage, ...) is still `[PLANNED]` — V0.2 built deal *assessment*, not automated wishlist matching yet |
| Collectors | Retailer adapters to the common schema | `collectors/` | `[PLANNED]`; not in V0.2 either (folder exists with a README, now pointing at the real V0.2 schema to target) |
| AI layer | Provider abstraction, preference parsing, explanations, review analysis | `ai/` | `[PLANNED]`; not in V0.2 (folder exists with a README only) |
| Notifications | Deliver alerts when conditions are met | `notifications/` (not yet created — see note below) | `[PLANNED]`; channels `[UNKNOWN]` |
| Automation | Background workers; later browser-assisted checkout | `automation/` | `[PLANNED]`; not in V0.2 (folder exists with a README only); checkout is late and human-gated |
| Tests | Backend: `backend/tests/` (pytest). Frontend: colocated under `frontend/src/` (Vitest) | `tests/` holds only a README explaining this split | `[VERIFIED]` 115 backend tests, 14 frontend tests — all passing as of 2026-10-01 (Linux sandbox; see CURRENT_STATE.md) |
| Docs | Developer and setup documentation | `README.md` (root) | `[BUILT]`, updated for V0.2 |
| Demo data | Optional, clearly-labelled fixture data for exercising the Data Explorer | `backend/scripts/seed_demo_data.py` | `[BUILT]` in V0.2; never run automatically (D-022) |
| Project memory | Vendor-independent project context | `project-memory/` | `[VERIFIED]` created 2026-09-21, updated 2026-09-26 and 2026-09-29 |

`notifications/` is a top-level folder in the Master Instructions' original suggested structure that still has no code and is left uncreated (no README placeholder either, since nothing yet references it the way collectors/ai/automation are referenced by name in both V0.1 and V0.2's briefs). `deal_engine` exists now, but as `backend/app/deal_engine/` rather than a top-level sibling folder — see D-023 for why. See section 13 for the full V0.2 tree.

## 4. Interfaces and boundaries
- **Collector to core.** Every collector returns the *common schema* (section 5) and nothing retailer-specific. Collectors do not write to the database directly; the core validates and stores their output. *[draft]*
- **Frontend and backend.** REST for requests; WebSocket for live updates (price, offer, stock, deal events) is still `[PLANNED]`. *[source: Master for WebSockets; the REST split is a draft]* **V0.1 actual:** REST only, over `fetch`, typed in `frontend/src/lib/api.ts`. The system-status panel polls `GET /api/health` every 15 seconds (`frontend/src/hooks/useHealth.ts`) rather than being pushed updates — a deliberate, simple interim measure until there's a WebSocket layer worth pushing over (see D-013 in DECISIONS.md region on V0.1 scope). CORS is configured in `backend/app/config.py` / `.env` so the Vite dev server can call the API in development.
- **AI provider interface.** One abstraction with an Ollama-compatible implementation first; another provider must be addable without changing callers. AI results come back as structured data and are validated before use. *[source: Master]*
- **Rule engine and AI.** The rule engine consumes only validated structured preferences and stored data. It never reads free-form AI text (D-003).
- **Deal engine to notifications/automation.** The deal engine emits events; notifications and automation react to events. They do not recompute prices. *[draft]*
- **Automation and the human.** Any security-sensitive checkout step (CAPTCHA, OTP, payment authorization) is a hand-off to the human (D-008).

## 5. Common data model — `[BUILT]` in V0.2 (was: conceptual draft)
This was a conceptual draft describing what the Master Instructions required, with schema/keys/types marked `[UNKNOWN]`. As of V0.2, most of it is real, implemented SQLModel tables — the list below is kept as the *conceptual* description (still useful as a quick summary), each entry now annotated with where the real thing lives. Full field lists and the actual schema: section 13.

- **Product / model**: brand, model name; linked to a normalized spec sheet. → `Product` (`backend/app/models/product.py`). No linked spec sheet yet — `description` is free text only; structured specs (SoC, display, camera, ...) are still `[PLANNED]`, see `KNOWLEDGE/phone-data.md`.
- **Variant**: the model plus the attributes that make offers comparable (RAM, storage; also condition, region, warranty). Color and seller are recorded too. Which attributes form the comparison key is open (OQ-3). → `ProductVariant` (storage_gb, ram_gb, color, unique per product) implements the RAM/storage/color part now; condition (new/refurbished/open-box), region, and warranty are not yet fields — OQ-3 is still only *partly* resolved (see section 11).
- **Retailer**, **Seller**. → `Retailer` is its own table. "Seller" is not a separate table -- it's `RetailerListing.seller_name`, a free-text field for marketplace sellers, not a normalized entity of its own.
- **Listing**: a retailer-specific URL/identifier mapped to a variant. → `RetailerListing` (product_url unique, external_listing_id, maps to exactly one ProductVariant and one Retailer).
- **Price observation**: product, variant, seller, retailer, price, MRP (when available), timestamp, availability, relevant offer information. → `PriceObservation` (observed_price, mrp, observed_at; scoped to a RetailerListing, which already implies variant/retailer/seller). Append-only — see D-013's module docstring reference and the price_observations router.
- **Offer**: type (instant discount, bank/card, exchange, coupon, EMI, membership, cashback, other), amount, conditions, certainty (guaranteed or conditional), source, observed-at. → `Offer` (offer_type, discount_amount/discount_percentage, is_guaranteed, conditions, valid_from/valid_until). No separate "source" field -- the retailer_listing_id it belongs to is the source.
- **Wishlist item / watch**: an exact target (product or variant) plus deterministic conditions (max price, minimum storage, required variant, availability, seller conditions). → Still V0.1's `Wishlist` (preferences, not a specific product/variant target). Linking a wishlist entry to a specific `ProductVariant` — the "watch" half of this — is still `[PLANNED]`; V0.2's deal-assessment endpoint takes an *ad hoc* `wishlist_id` query parameter instead of a stored link (see D-020's consequences).
- **User preferences (structured)**: unchanged, still `Wishlist`'s fields from V0.1.
- **Deal event**: price drop, record low, offer change, stock change, new discovery, with the reasons that triggered it. → Not a stored entity. `DealAssessment` (computed, not stored — D-020) covers "price drop" and "record low" as signals; "offer change", "stock change", and "new discovery" as *events over time* are still `[PLANNED]` (need an events/notifications system that doesn't exist yet).
- **Spec sheet**: normalized phone specifications with per-field source and certainty (see `KNOWLEDGE/phone-data.md`). → Still `[PLANNED]`; not part of V0.2.

## 6. Deterministic price and deal rules *[source: Master; `[BUILT]` in V0.2 — see `backend/app/deal_engine/assessment.py`]*
Price components, never blended silently:
1. **Base price**: the actual listed selling price. → `DealAssessment.current_price`.
2. **Guaranteed discount**: clearly applicable without uncertain requirements. → `guaranteed_discount_total`, from `Offer.is_guaranteed=true` (excluding cashback-type offers, which are their own total regardless of guarantee — see rule 4 and D-006).
3. **Conditional discount**: specific bank card, exchange, coupon, EMI, membership, limited eligibility. → `conditional_discount_total`, from `Offer.is_guaranteed=false`.
4. **Cashback**: tracked separately; never auto-subtracted when uncertain. → `cashback_total`, from `Offer.offer_type="cashback"`; excluded from both discount totals and from `effective_price_guaranteed` even when `is_guaranteed=true` on the cashback offer itself.

When conditions are not guaranteed, show a **"Potential effective price"** → `potential_effective_price`, only populated when a conditional discount actually exists (not duplicated as the same number when there's nothing conditional to show).

History metrics: **implemented** — current price, lowest observed, highest observed, average (all-time, scoped to one listing). **Not yet implemented** — "recent average" specifically (as distinct from the all-time average), and the 7/30/90-day low windows; V0.2's `price_dropped_from_previous_observation` and `lowest_observed_in_history` cover "is this better than before" without needing fixed time windows, which was enough for V0.2's scope, but doesn't replace those specific metrics if a future version wants them. OQ-4 (the "recent average" window definition) is therefore still open.

Wording rule: say "all-time low" only if stored history supports it; otherwise say "lowest observed in our history". **Implemented literally** — `assessment.py` never emits the phrase "all-time low" anywhere, only "lowest observed in our history" wording, and only once there are at least 2 observations to make the comparison meaningful (see D-005; tested in `test_deal_engine.py::test_never_claims_all_time_low_wording`). Deal quality is judged against stored history, not the advertised MRP — **implemented**: an MRP discount is surfaced only as an informational caveat, never as a `reasons` entry (tested in `test_mrp_discount_alone_is_labelled_a_caveat_not_a_reason`).

## 7. AI layer rules
- May do: interpret requirements, classify, summarize, discover alternatives, explain deals and price history, analyze reviews, flag suspicious listing information. *[source: Master]*
- May not: decide maximum price, minimum storage, required variant, availability, seller conditions, or any financial action. *[source: Master]*
- Output must be structured and schema-validated before use (a listed test area).
- Local-first: Ollama-compatible; no dependency on a paid AI API.
- *[architect note, 2026-09-21]* Text scraped from retailer pages and reviews is untrusted data. Never treat it as instructions to the model or to automation.

## 8. Technology choices *[source: Master, "preferred initial stack"]*

| Area | Choice | Rationale recorded |
|---|---|---|
| Frontend | React, Vite, TypeScript, Tailwind CSS, Framer Motion, Lucide | Not recorded beyond "preferred" |
| Backend | Python, FastAPI, asyncio | Async I/O is a stated performance preference |
| Database | SQLite (initially) | Not recorded |
| Browser automation | Playwright | Not recorded |
| Realtime | WebSockets | Live dashboard updates (stated) |
| AI | Ollama-compatible architecture, provider abstraction | No dependence on a paid AI API (stated) |
| Target runtime | A Windows PC, run locally | Stated |

**V0.1 specifics** (see D-013 to D-017 in DECISIONS.md for the reasoning behind each):
- Backend uses **SQLModel** (SQLAlchemy + Pydantic combined) rather than bare SQLAlchemy, to avoid duplicating field definitions between the database table and the API request/response schemas (D-013).
- No migration tool yet; `SQLModel.metadata.create_all()` builds tables from the model classes directly (D-013). Introduce Alembic (or similar) before this matters for real data — this was OQ-5 below, now a recorded, deliberate gap rather than an open question.
- Frontend uses **Tailwind v3** (not v4) and does **not** include Framer Motion — both conservative choices made without the ability to verify newer tooling in a network-disconnected build environment (D-016). Motion needs are small enough to cover with Tailwind transitions and a couple of CSS keyframes.
- Fonts: **IBM Plex Sans** for UI text, **IBM Plex Mono** reserved specifically for numeric/data values (prices, specs) — never for decorative labels (D-017).

**V0.2 specifics** (see D-018 to D-024 in DECISIONS.md):
- No SQLModel `Relationship()` declarations anywhere in the new models — plain foreign keys, explicit `select()` queries in the service layer (D-018).
- `availability` and `offer_type` are plain `str` columns; the allowed-value sets live as `typing.Literal` aliases in `app/models/enums.py`, enforced only at the Pydantic Create/Update layer, not as a database-level `Enum` type (D-019).
- Deal assessment is computed on request (`app/deal_engine/assess_deal()`), never stored (D-020).
- Deletes that would orphan price history are blocked (409), not cascaded — enforced by an explicit service-layer check plus SQLite foreign-key enforcement (`PRAGMA foreign_keys=ON`) as a backstop (D-021).
- Demo/fixture data (`backend/scripts/seed_demo_data.py`) uses real retailer names as reference data but an always-fictional product, with a real `is_demo` database column plus visible frontend badging — never a real phone model with fake prices (D-022).
- `deal_engine` is `backend/app/deal_engine/`, a subpackage of the backend, not a top-level sibling folder like the Master Instructions' original sketch suggested (D-023).
- The "latest price per listing" query fetches and reduces in Python rather than using a SQL window function, since SQLite window-function support depends on the specific build and couldn't be confirmed without running it (D-024).

## 9. Performance approach *[source: Master]*
Async I/O; concurrent collectors where appropriate; persistent browser sessions where appropriate; caching; incremental updates; background workers; WebSockets for live updates; minimal repeated network requests; efficient database queries; debounced UI updates. Do not relaunch browsers unnecessarily. Do not scan every product when exact product URLs or identifiers are known.

## 10. Security boundaries *[source: Master]*
- Never request or store passwords, UPI PINs, card CVVs, OTPs or authentication secrets.
- No CAPTCHA bypassing. No anti-bot circumvention. If a retailer blocks or challenges a collector, degrade (mark data stale or uncertain, tell the user) instead of evading.
- CAPTCHA, OTP, payment authorization and similar confirmations stay human-controlled.
- Configuration through environment variables; `.env.example` instead of hardcoded secrets.

## 11. Open architectural questions
- **OQ-1** ~~The repository layout as it actually exists~~ **RESOLVED** — see sections 12 (V0.1) and 13 (V0.2).
- **OQ-2** `[UNKNOWN]` Background-work mechanism (asyncio tasks inside the API process vs a separate worker process), and how collectors are scheduled and rate-limited. Not touched in V0.2 — no collectors exist yet. (`deal_engine`'s own location question is separately resolved — D-023.)
- **OQ-3** **Partly resolved in V0.2.** The RAM/storage/color part of the variant identity key is now real: `ProductVariant` has a unique constraint on `(product_id, storage_gb, ram_gb, color)` (see D-013's module docstring and `test_product_variants.py::test_different_configs_do_not_collapse_into_one_variant`). Still open: condition (new/refurbished/open-box), region, and warranty are not yet fields on `ProductVariant` at all — the original proposal (model + RAM + storage + condition + region, with color/seller/warranty as attributes) is only half-built. Also still open: how a `Wishlist` entry would ever get *linked* to a specific `Product`/`ProductVariant` it's shopping for (matching) — V0.2's deal-assessment endpoint sidesteps this by taking an ad hoc `wishlist_id` per request rather than a stored link (see section 5).
- **OQ-4** `[UNKNOWN]` Definition of "recent average" (window length), and the 7/30/90-day low windows. V0.2 implements all-time lowest/highest/average and "better or worse than the previous observation", which didn't require settling this, but doesn't resolve it either — still open for whenever fixed-window metrics are wanted (see section 6).
- **OQ-5** **Deliberately deferred, not resolved** — still `SQLModel.metadata.create_all()` with no migration tool (D-013), now covering six more tables than V0.1. Pick and introduce one (e.g. Alembic) before schema changes need to preserve real data — more pressing now than in V0.1, given V0.2 has real price-history and offer data to lose if a future model change needs one.
- **OQ-6** `[UNKNOWN]` Notification channels available on a local Windows setup. Not touched in V0.2.
- **OQ-7** `[UNKNOWN]` How persistent browser sessions coexist with "never store authentication secrets". Not touched in V0.2 — no browser automation exists yet.
- **OQ-8** `[UNKNOWN]` How Hunt Mode changes polling and priority (frequency, which targets, which retailers). Not touched in V0.2 — no Hunt Mode UI exists yet.
- **OQ-9** ~~How the frontend and backend are started and served on Windows~~ **RESOLVED for development** — unchanged from V0.1; see the root `README.md`.
- **OQ-10** ~~Whether uniqueness-constraint violations should get a friendly error~~ **RESOLVED 2026-10-01** — they return HTTP 409 via `commit_unique()` / `DuplicateRecordError` (D-026).

## 12. Actual layout (V0.1) — `[BUILT]`

Written from direct inspection of the repository built in this session (2026-09-26), not from the Master Instructions' suggested tree. Status tag meaning: `[BUILT]` = written and passed offline static checks (Python: `py_compile` on every file; TypeScript/TSX: parsed with the TypeScript compiler's own parser on every file) but **not yet confirmed by actually running it** — see CURRENT_STATE.md for exactly what that means and why.

```
BBD/
├── README.md                    setup, run, and test instructions
├── .gitignore
├── project-memory/               this memory layer
├── backend/
│   ├── app/
│   │   ├── main.py                FastAPI app + CORS + lifespan (calls init_db on startup)
│   │   ├── config.py               Settings (pydantic-settings), env-var driven
│   │   ├── database.py             SQLite engine, session dependency, init_db()
│   │   ├── utils.py                 shared helpers: utcnow() (timezone-aware UTC), ensure_utc(), UTCDatetime (D-025)
│   │   ├── models/wishlist.py        WishlistBase/Wishlist/Create/Update/Read (SQLModel)
│   │   ├── routers/health.py          GET /api/health (a real DB check, not hardcoded)
│   │   ├── routers/wishlists.py        full CRUD, /api/wishlists
│   │   └── services/wishlist_service.py  validation + persistence, separate from routes
│   ├── tests/                     18 pytest tests (conftest.py, test_health.py, test_wishlists.py)
│   ├── requirements.txt            minimum-version pins (see file header for why)
│   ├── pytest.ini
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.tsx, App.tsx        entry point and dashboard layout
│   │   ├── components/layout/        Header, StatusDot, SystemStatusPanel
│   │   ├── components/hunt/           HuntInput (hero: natural-language box + optional exact-constraints panel)
│   │   ├── components/wishlist/        WishlistPanel, WishlistItem
│   │   ├── components/deals/            DealFeed (honest empty state, D-005)
│   │   ├── components/activity/          ActivityLog (session-only, not persisted)
│   │   ├── hooks/                    useHealth (polls), useWishlists (CRUD), useActivityLog
│   │   ├── lib/api.ts                  typed fetch wrapper
│   │   └── types/wishlist.ts            TypeScript types mirroring the backend schemas by hand
│   ├── App.test.tsx, hooks/useHealth.test.ts   8 Vitest tests total
│   ├── package.json                  caret-range pins (see file for why)
│   └── tailwind.config.js             design tokens — see D-017
├── collectors/README.md, ai/README.md, automation/README.md   empty on purpose; each explains what will go there
├── database/README.md              bbd_hunter.db is created here at runtime, gitignored
└── tests/README.md                  explains why tests live in backend/ and frontend/src/ instead
```

**What exists and is wired together end-to-end (`[VERIFIED]` live 2026-10-01 against a real server):** natural-language hunt input → `POST /api/wishlists` → SQLite → `GET /api/wishlists` → wishlist panel. Health/status polling → system-status panel (Backend and Database are live checks; AI and Collectors are honest static "not connected"/"not running" labels, matching D-005's rule against inventing state).

**What does not exist yet (as of V0.1):** anything under `deal_engine/`, price/offer/history logic, collectors, the AI layer, notifications, Hunt Mode, and a frontend edit UI for wishlist entries (the backend `PUT` endpoint and the frontend `useWishlists().edit()` action both exist and are tested, but no button calls it yet — see TODO.md). **Most of this is no longer true as of V0.2 — see section 13.**

## 13. Actual layout (V0.2 additions) — `[VERIFIED]` 2026-10-01 (Linux sandbox; Windows re-run pending)

**Datetime convention (D-025):** every timestamp is timezone-aware UTC. `utcnow()` is aware; API input fields use `UTCDatetime` (offsets converted, naive = UTC); SQLModel's `UTCDateTime` column returns aware UTC on read, including from SQLite. Error mapping: `NotFoundReferenceError` → 422, `HasDependentsError` → 409, `DuplicateRecordError` → 409, all in `main.py`.

Written from direct inspection of the repository built in this session (2026-09-29). Shows only what V0.2 *added* to section 12's V0.1 tree — the actual V0.1 *files* are unchanged (every one was diffed byte-for-byte against the V0.1 delivery before any V0.2 edit began, confirming none were accidentally touched, as this update's "preserve V0.1" instruction required); this memory file's own section 12 got one small addition (a pointer to this section) but its tree diagram is untouched. Combined, sections 12 + 13 are the complete current tree. Same `[BUILT]` meaning as section 12: passed offline static checks, not yet confirmed by actually running it.

```
BBD/
├── README.md                        updated: V0.2 section, new API table, seed-data instructions, updated verification note
├── backend/
│   ├── app/
│   │   ├── main.py                    +V0.2 routers, shared NotFoundReferenceError (422) / HasDependentsError (409) / DuplicateRecordError (409) exception handlers
│   │   ├── config.py                   app_version bumped to 0.2.0
│   │   ├── database.py                 +SQLite PRAGMA foreign_keys=ON (D-021); init_db() imports the 6 new model modules
│   │   ├── normalization.py            NEW: deterministic product-name parsing (brand/RAM/storage/color)
│   │   ├── deal_engine/
│   │   │   ├── __init__.py               exports DealAssessment, DealSignals, assess_deal
│   │   │   └── assessment.py              NEW: the deal assessment logic itself (D-020)
│   │   ├── models/
│   │   │   ├── enums.py                  NEW: AvailabilityStatus / OfferType Literal aliases (D-019)
│   │   │   ├── retailer.py                NEW: Retailer (+Create/Update/Read)
│   │   │   ├── product.py                  NEW: Product (+Create/Update/Read/ListItem/Detail)
│   │   │   ├── product_variant.py           NEW: ProductVariant (+Create/Update/Read)
│   │   │   ├── retailer_listing.py           NEW: RetailerListing (+Create/Update/Read/ListItem)
│   │   │   ├── price_observation.py           NEW: PriceObservation (+Create/Read) -- append-only
│   │   │   └── offer.py                        NEW: Offer (+Create/Update/Read)
│   │   ├── routers/                    NEW: retailers.py, products.py, product_variants.py, retailer_listings.py (+deal-assessment endpoint), price_observations.py, offers.py
│   │   └── services/
│   │       ├── errors.py                 NEW: NotFoundReferenceError, HasDependentsError (D-021), DuplicateRecordError (D-026)
│   │       ├── db_helpers.py              NEW (2026-10-01): commit_unique() — unique violation -> DuplicateRecordError -> 409
│   │       └── (one *_service.py NEW per entity above, mirroring the V0.1 wishlist_service.py pattern)
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── seed_demo_data.py           NEW: optional, clearly-labelled demo data (D-022) -- never run automatically
│   └── tests/                        +81 new tests: test_normalization.py, test_retailers.py, test_products.py,
│                                        test_product_variants.py, test_retailer_listings.py,
│                                        test_price_observations.py, test_offers.py, test_deal_engine.py;
│                                        2026-10-01: +test_datetimes.py (10), +test_duplicate_conflicts.py (6); conftest.py now enables
│                                        PRAGMA foreign_keys=ON on the test engine. 115 backend tests total, all passing.
├── frontend/
│   └── src/
│       ├── App.tsx                    changed: Dashboard/Data Explorer tab switch (Header now takes activeView/onViewChange)
│       ├── App.test.tsx                +1 test for the tab switch; all V0.1 tests unchanged
│       ├── test/setup.ts                 2026-10-01: jest-dom/vitest entry + explicit RTL cleanup (BUG-002, D-027)
│       ├── components/layout/Header.tsx  changed: renders the two-tab nav; branding unchanged
│       ├── components/explorer/        NEW: DataExplorer.tsx (drill-down container + selection state),
│       │                                  ProductListPanel, VariantListPanel, ListingsPanel, PriceHistoryList,
│       │                                  OffersList, DealSignalsSummary, DemoBadge, DataExplorer.test.tsx (5 tests)
│       ├── hooks/useFetch.ts             NEW: small generic fetch-on-mount hook
│       ├── hooks/useExplorerData.ts       NEW: useProducts, useRetailers, useProductDetail, useListingsForVariant,
│       │                                    usePriceHistory, useOffersForListing, useDealAssessment (all built on useFetch)
│       ├── lib/api.ts                   +V0.2 read functions (listProducts, getProductDetail, listRetailers,
│       │                                  listRetailerListings, listPriceObservations, listOffers, getDealAssessment);
│       │                                  all V0.1 functions unchanged
│       └── types/product.ts             NEW: TypeScript types mirroring the V0.2 backend schemas
│           (types/wishlist.ts unchanged from V0.1)
└── collectors/README.md              updated: now points at the real V0.2 schema and the normalization/deal_engine modules
```

**What's wired together end-to-end, on top of V0.1's chain (API `[VERIFIED]` live 2026-10-01; the UI itself verified by jsdom tests + build, not yet in a real browser):** Products -> (click) -> Variants -> (click) -> Retailer Listings (with a real, batched latest-price lookup) -> (click) -> Price History + Offers + Deal Signals, all fetched live from the backend, all showing an honest empty state ("No price history available yet.", "No offers available.") rather than fabricated data when there's nothing to show. `GET /api/retailer-listings/{id}/deal-assessment` is real, computed, and testable independent of the frontend.

**What still does not exist:** collectors (still just a README), the AI layer, notifications, Hunt Mode, the events/deal-event history described in section 5, structured phone specs (`KNOWLEDGE/phone-data.md`), and a frontend edit UI for wishlist entries (unchanged from V0.1). The deal engine assesses one listing at a time on request; it does not yet scan the whole database looking for deals matching a wishlist unprompted (that's "discover deals the user didn't explicitly add" from the original Master Instructions -- still future work).
