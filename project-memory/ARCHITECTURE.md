# BBD HUNTER — Architecture

> Purpose: the system architecture — components, data flow, interfaces, boundaries, technology choices.
> Last updated: 2026-09-21 · Memory layer V0.1

**STATUS: INTENDED architecture, not verified against code.** No repository was available when this file was written. Everything below comes from the Master Project Instructions (marked *[source: Master]*) or is a clearly labelled *[architect note]* or *[draft]* awaiting the user's approval. When the real repository is inspected, add an "Actual layout" section and record any differences (TODO T-001).

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

| Component | Responsibility | Intended location | Status |
|---|---|---|---|
| Frontend | Premium dashboard; Normal and Hunt Mode UIs; live updates | `frontend/` | `[PLANNED]` shell in V0.1; `[UNVERIFIED]` whether it exists |
| Backend API | HTTP + WebSocket API, orchestration, health/status | `backend/` | `[PLANNED]` shell in V0.1; `[UNVERIFIED]` |
| Database | SQLite persistence, schema, history queries | `database/` | `[PLANNED]` shell in V0.1; `[UNVERIFIED]` |
| Collectors | Retailer adapters to the common schema | `collectors/` | `[PLANNED]` not in V0.1 |
| Deal engine | Price components, history metrics, deal detection, rule engine | `deal_engine/` | `[PLANNED]` |
| AI layer | Provider abstraction, preference parsing, explanations, review analysis | `ai/` | `[PLANNED]` |
| Notifications | Deliver alerts when conditions are met | `notifications/` | `[PLANNED]`; channels `[UNKNOWN]` |
| Automation | Background workers; later browser-assisted checkout | `automation/` | `[PLANNED]`; checkout is late and human-gated |
| Tests | Unit and integration tests per component | `tests/` | `[PLANNED]` |
| Docs | Developer and setup documentation | `docs/` | `[PLANNED]` for V0.1 |
| Project memory | Vendor-independent project context | `project-memory/` | `[VERIFIED]` created 2026-09-21 |

The folder names come from the Master Instructions, which say the exact structure may evolve after architectural review.

## 4. Interfaces and boundaries
- **Collector to core.** Every collector returns the *common schema* (section 5) and nothing retailer-specific. Collectors do not write to the database directly; the core validates and stores their output. *[draft]*
- **Frontend and backend.** REST for requests; WebSocket for live updates (price, offer, stock, deal events). The frontend debounces UI updates. *[source: Master for WebSockets and debouncing; the REST split is a draft]*
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

## 9. Performance approach *[source: Master]*
Async I/O; concurrent collectors where appropriate; persistent browser sessions where appropriate; caching; incremental updates; background workers; WebSockets for live updates; minimal repeated network requests; efficient database queries; debounced UI updates. Do not relaunch browsers unnecessarily. Do not scan every product when exact product URLs or identifiers are known.

## 10. Security boundaries *[source: Master]*
- Never request or store passwords, UPI PINs, card CVVs, OTPs or authentication secrets.
- No CAPTCHA bypassing. No anti-bot circumvention. If a retailer blocks or challenges a collector, degrade (mark data stale or uncertain, tell the user) instead of evading.
- CAPTCHA, OTP, payment authorization and similar confirmations stay human-controlled.
- Configuration through environment variables; `.env.example` instead of hardcoded secrets.

## 11. Open architectural questions (all `[UNKNOWN]`)
- **OQ-1** The repository layout as it actually exists, and whether it matches section 3.
- **OQ-2** Background-work mechanism (asyncio tasks inside the API process vs a separate worker process), and how collectors are scheduled and rate-limited.
- **OQ-3** Variant identity key: which attributes make two listings comparable. Proposal: model + RAM + storage + condition + region, with color, seller and warranty as attributes.
- **OQ-4** Definition of "recent average" (window length).
- **OQ-5** Database migration approach.
- **OQ-6** Notification channels available on a local Windows setup.
- **OQ-7** How persistent browser sessions coexist with "never store authentication secrets". Default proposal: collectors use logged-out sessions, and the app never reads or copies the user's own logged-in browser profile. Decide before any logged-in browser use.
- **OQ-8** How Hunt Mode changes polling and priority (frequency, which targets, which retailers).
- **OQ-9** How the frontend and backend are started and served on Windows (two dev servers vs a bundled build).
