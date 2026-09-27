# BBD HUNTER — Architecture

> Purpose: the system architecture — components, data flow, interfaces, boundaries, technology choices.
> Last updated: 2026-09-26 · Memory layer V0.1 · Project version: V0.1 (built, not yet run live — see CURRENT_STATE.md)

**STATUS: mixed.** Section 12 ("Actual layout (V0.1)") describes what was actually built and is `[BUILT]` (written, passed offline static checks — syntax, cross-file references — but not yet confirmed by actually running it; see CURRENT_STATE.md). Everything else in this file is either still-intended architecture from the Master Project Instructions (marked *[source: Master]*), a labelled *[architect note]* or *[draft]*, or explicitly resolved/updated for V0.1 where noted. T-001 (reconcile memory with the real repository) is now done for the first time — this file, CURRENT_STATE.md, DECISIONS.md and TODO.md were all updated from direct inspection of the repository built in this session, not guessed.

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

## 3. Components

| Component | Responsibility | Actual/intended location | Status |
|---|---|---|---|
| Frontend | Dashboard shell: hunt input, wishlist, live system status, honest empty deal feed, session activity log | `frontend/` | `[BUILT]` V0.1 foundation (no Hunt Mode UI yet, no live product data) |
| Backend API | HTTP API, config, health/status, wishlist CRUD | `backend/` | `[BUILT]` V0.1 foundation (REST only; no WebSocket yet) |
| Database | SQLite persistence for the wishlist table | `database/` | `[BUILT]` V0.1 (one table; no migrations yet — see D-013) |
| Collectors | Retailer adapters to the common schema | `collectors/` | `[PLANNED]`; not in V0.1 (folder exists with a README only) |
| Deal engine | Price components, history metrics, deal detection, rule engine | `deal_engine/` (not yet created — see note below) | `[PLANNED]` |
| AI layer | Provider abstraction, preference parsing, explanations, review analysis | `ai/` | `[PLANNED]`; not in V0.1 (folder exists with a README only) |
| Notifications | Deliver alerts when conditions are met | `notifications/` (not yet created — see note below) | `[PLANNED]`; channels `[UNKNOWN]` |
| Automation | Background workers; later browser-assisted checkout | `automation/` | `[PLANNED]`; not in V0.1 (folder exists with a README only); checkout is late and human-gated |
| Tests | Backend: `backend/tests/` (pytest). Frontend: colocated under `frontend/src/` (Vitest) | `tests/` holds only a README explaining this split | `[BUILT]` 18 backend tests, 8 frontend tests (all `[BUILT]`, not yet run live — see CURRENT_STATE.md) |
| Docs | Developer and setup documentation | `README.md` (root) | `[BUILT]` for V0.1 |
| Project memory | Vendor-independent project context | `project-memory/` | `[VERIFIED]` created 2026-09-21, updated 2026-09-26 |

`deal_engine/` and `notifications/` are top-level folders in the Master Instructions' original suggested structure, but the V0.1 implementation brief's own target tree doesn't list them, and V0.1 has no code for either yet. They're left uncreated for now rather than added as empty placeholders; see section 12 for the tree actually built. The folder names may still evolve after further architectural review.

## 4. Interfaces and boundaries
- **Collector to core.** Every collector returns the *common schema* (section 5) and nothing retailer-specific. Collectors do not write to the database directly; the core validates and stores their output. *[draft]*
- **Frontend and backend.** REST for requests; WebSocket for live updates (price, offer, stock, deal events) is still `[PLANNED]`. *[source: Master for WebSockets; the REST split is a draft]* **V0.1 actual:** REST only, over `fetch`, typed in `frontend/src/lib/api.ts`. The system-status panel polls `GET /api/health` every 15 seconds (`frontend/src/hooks/useHealth.ts`) rather than being pushed updates — a deliberate, simple interim measure until there's a WebSocket layer worth pushing over (see D-013 in DECISIONS.md region on V0.1 scope). CORS is configured in `backend/app/config.py` / `.env` so the Vite dev server can call the API in development.
- **AI provider interface.** One abstraction with an Ollama-compatible implementation first; another provider must be addable without changing callers. AI results come back as structured data and are validated before use. *[source: Master]*
- **Rule engine and AI.** The rule engine consumes only validated structured preferences and stored data. It never reads free-form AI text (D-003).
- **Deal engine to notifications/automation.** The deal engine emits events; notifications and automation react to events. They do not recompute prices. *[draft]*
- **Automation and the human.** Any security-sensitive checkout step (CAPTCHA, OTP, payment authorization) is a hand-off to the human (D-008).

## 5. Common data model (conceptual draft; not implemented)
Entities and the fields the Master Instructions require. Exact schema, keys and types are `[UNKNOWN]` until designed (proposed for V0.2).

- **Product / model**: brand, model name; linked to a normalized spec sheet.
- **Variant**: the model plus the attributes that make offers comparable (RAM, storage; also condition, region, warranty). Color and seller are recorded too. Which attributes form the comparison key is open (OQ-3).
- **Retailer**, **Seller**.
- **Listing**: a retailer-specific URL/identifier mapped to a variant.
- **Price observation**: product, variant, seller, retailer, price, MRP (when available), timestamp, availability, relevant offer information.
- **Offer**: type (instant discount, bank/card, exchange, coupon, EMI, membership, cashback, other), amount, conditions, certainty (guaranteed or conditional), source, observed-at.
- **Wishlist item / watch**: an exact target (product or variant) plus deterministic conditions (max price, minimum storage, required variant, availability, seller conditions).
- **User preferences (structured)**: budget target, budget maximum, storage minimum, RAM preference, camera / gaming / battery priorities, wireless-charging preference, software preference, brand preference.
- **Deal event**: price drop, record low, offer change, stock change, new discovery, with the reasons that triggered it.
- **Spec sheet**: normalized phone specifications with per-field source and certainty (see `KNOWLEDGE/phone-data.md`).

## 6. Deterministic price and deal rules *[source: Master]*
Price components, never blended silently:
1. **Base price**: the actual listed selling price.
2. **Guaranteed discount**: clearly applicable without uncertain requirements.
3. **Conditional discount**: specific bank card, exchange, coupon, EMI, membership, limited eligibility.
4. **Cashback**: tracked separately; never auto-subtracted when uncertain.

When conditions are not guaranteed, show a **"Potential effective price"**, labelled as conditional.

History metrics per variant: current price, lowest observed, highest observed, average, recent average, 7-day low, 30-day low, 90-day low, percentage change, distance from historical low. The window for "recent average" is `[UNKNOWN]` (OQ-4).

Wording rule: say "all-time low" only if stored history supports it; otherwise say "lowest observed in our history". Deal quality is judged against stored history, not the advertised MRP.

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
- No migration tool yet; `SQLModel.metadata.create_all()` builds tables from the model classes directly (D-013). Introduce Alembic (or similar) before this matters for real data — this was OQ-5 below, now a recorded, deliberate V0.1 gap rather than an open question.
- Frontend uses **Tailwind v3** (not v4) and does **not** include Framer Motion in V0.1 — both conservative choices made without the ability to verify newer tooling in a network-disconnected build environment (D-016). Motion needs in V0.1 are small enough to cover with Tailwind transitions and a couple of CSS keyframes.
- Fonts: **IBM Plex Sans** for UI text, **IBM Plex Mono** reserved specifically for numeric/data values (prices, specs) — never for decorative labels (D-017).

## 9. Performance approach *[source: Master]*
Async I/O; concurrent collectors where appropriate; persistent browser sessions where appropriate; caching; incremental updates; background workers; WebSockets for live updates; minimal repeated network requests; efficient database queries; debounced UI updates. Do not relaunch browsers unnecessarily. Do not scan every product when exact product URLs or identifiers are known.

## 10. Security boundaries *[source: Master]*
- Never request or store passwords, UPI PINs, card CVVs, OTPs or authentication secrets.
- No CAPTCHA bypassing. No anti-bot circumvention. If a retailer blocks or challenges a collector, degrade (mark data stale or uncertain, tell the user) instead of evading.
- CAPTCHA, OTP, payment authorization and similar confirmations stay human-controlled.
- Configuration through environment variables; `.env.example` instead of hardcoded secrets.

## 11. Open architectural questions
- **OQ-1** ~~The repository layout as it actually exists~~ **RESOLVED for V0.1** — see section 12.
- **OQ-2** `[UNKNOWN]` Background-work mechanism (asyncio tasks inside the API process vs a separate worker process), and how collectors are scheduled and rate-limited. Not touched in V0.1 — no collectors exist yet.
- **OQ-3** `[UNKNOWN]` Variant identity key: which attributes make two listings comparable. Proposal unchanged: model + RAM + storage + condition + region, with color, seller and warranty as attributes. Not touched in V0.1 — the wishlist model stores a shopper's *preferences* (e.g. "at least 256GB"), not a specific product/variant to match against; product/variant entities don't exist yet (see REQUIREMENTS.md V0.2 scope).
- **OQ-4** `[UNKNOWN]` Definition of "recent average" (window length). Not relevant yet — no price history exists.
- **OQ-5** **Deliberately deferred, not resolved** — V0.1 uses `SQLModel.metadata.create_all()` with no migration tool (D-013). Pick and introduce one (e.g. Alembic) before schema changes need to preserve real user data.
- **OQ-6** `[UNKNOWN]` Notification channels available on a local Windows setup. Not touched in V0.1.
- **OQ-7** `[UNKNOWN]` How persistent browser sessions coexist with "never store authentication secrets". Default proposal unchanged: collectors use logged-out sessions, and the app never reads or copies the user's own logged-in browser profile. Decide before any logged-in browser use. Not touched in V0.1 — no browser automation exists yet.
- **OQ-8** `[UNKNOWN]` How Hunt Mode changes polling and priority (frequency, which targets, which retailers). Not touched in V0.1 — no Hunt Mode UI exists yet.
- **OQ-9** ~~How the frontend and backend are started and served on Windows~~ **RESOLVED for development** — two separate dev servers (`uvicorn app.main:app --reload` and `npm run dev`), run in separate terminals; exact commands in the root `README.md`. How this looks for a non-technical end user (one launcher vs two terminals) is still open for a later phase.

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
│   │   ├── utils.py                 shared utcnow() helper
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

**What exists and is wired together end-to-end (pending a live run to confirm):** natural-language hunt input → `POST /api/wishlists` → SQLite → `GET /api/wishlists` → wishlist panel. Health/status polling → system-status panel (Backend and Database are live checks; AI and Collectors are honest static "not connected"/"not running" labels, matching D-005's rule against inventing state).

**What does not exist yet:** anything under `deal_engine/`, price/offer/history logic, collectors, the AI layer, notifications, Hunt Mode, and a frontend edit UI for wishlist entries (the backend `PUT` endpoint and the frontend `useWishlists().edit()` action both exist and are tested, but no button calls it yet — see TODO.md).
