# BBD HUNTER — Decision Log

> Purpose: append-only history of architectural and product decisions. Never edit or delete an old entry. To change a decision, add a new entry at the bottom and mark the old one "Superseded by D-###".
> Last updated: 2026-09-26 · Memory layer V0.1

**Provenance.** D-001 to D-010 and D-012 come from the user's Master Project Instructions. Their original decision dates are `[UNKNOWN]`, so they carry the day they were first recorded here (2026-09-21). D-011 comes from the Project Memory Layer V0.1 brief. "Alternatives considered" is filled in only where the source states one; otherwise the entry says so. "Consequences" are expected implications, some labelled *architect note*.

Status values: Accepted · Proposed · Superseded by D-###

---

## D-001 — Local-first architecture
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: The application runs locally on a Windows PC. No paid cloud backend is required; external services are optional.
- **Reason**: Stated goal: run on a Windows PC without a paid cloud backend, and avoid unnecessary cloud dependencies.
- **Alternatives considered**: Not recorded. Excluded by instruction: a required paid cloud backend.
- **Consequences**: Storage, rules, collection and AI must work on one machine. Local hardware limits model size and speed (hardware `[UNKNOWN]`). Deployment means copying the project to Windows and running it, so setup steps must be documented exactly.

## D-002 — Preferred initial technology stack
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Frontend: React, Vite, TypeScript, Tailwind CSS, Framer Motion, Lucide icons. Backend: Python, FastAPI, asyncio. Database: SQLite initially. Browser automation: Playwright. Realtime: WebSockets. AI: Ollama-compatible architecture with local models where practical, behind a provider abstraction so another model can be added later.
- **Reason**: Given as the "preferred initial stack". Detailed rationale is not recorded. Stated goals it serves: performance (async I/O, WebSockets), local-first operation, no paid AI API.
- **Alternatives considered**: Not recorded. Excluded by instruction: dependence on a paid AI API.
- **Consequences**: Node (frontend tooling) and Python (backend) both need installing on Windows, with exact commands documented. Playwright needs a one-time browser download. *Architect note:* SQLite is simple but limits concurrent writes; revisit if many collectors write at once (RQ-06).

## D-003 — AI safety architecture: AI interprets, deterministic rules decide
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Pipeline: USER → AI interpretation → structured preferences → deterministic rule engine → deal engine → automation. Deterministic rules own maximum price, minimum storage, required variant, required availability, required seller conditions and explicit user constraints. AI owns interpretation, classification, summarization, discovery, explanation and review analysis.
- **Reason**: Stated: an LLM must not directly determine financial actions based solely on free-form reasoning.
- **Alternatives considered**: Not recorded. Excluded by instruction: LLM-only decisions on financial actions.
- **Consequences**: AI output must be schema-validated before use (a listed test area). The rule engine and deal engine need thorough tests. If the AI fails, explanations degrade but alert correctness does not.

## D-004 — Isolated retailer collector adapters with a common schema
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: One adapter per retailer (flipkart, amazon, croma, reliance, vijaysales, generic), each normalizing output into a common product schema. Collector code is isolated from the rest of the application.
- **Reason**: Stated: the application must not depend on any one retailer's HTML structure.
- **Alternatives considered**: Not recorded. Excluded by instruction: making the whole application depend on one retailer's HTML structure.
- **Consequences**: A stable common schema is needed before the first collector. A retailer page change affects one adapter only. Each adapter needs contract tests against the schema.

## D-005 — Data honesty and uncertainty rules
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Never invent prices, discounts, specifications, availability or offers. Mark uncertain information as uncertain. An advertised MRP discount is not proof of a genuine deal. Say "all-time low" only when stored history supports it; otherwise say "lowest observed in our history".
- **Reason**: Stated: the application must prioritize factual price information and transparent calculations.
- **Alternatives considered**: Not recorded. Excluded by instruction: treating an MRP discount as proof of a genuine deal; claiming an all-time low without supporting history.
- **Consequences**: Derived values need provenance and an uncertainty state. The UI needs a clear "uncertain" presentation. Claims about history depend on how much history exists, so a new install has a cold-start limit (RQ-04).

## D-006 — Separate price components
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Keep base price, guaranteed discount, conditional discount (specific bank card, exchange, coupon, EMI, membership, limited eligibility) and cashback separate. Never auto-subtract uncertain cashback. When conditions are not guaranteed, show "Potential effective price".
- **Reason**: Stated: transparent, honest deal calculation.
- **Alternatives considered**: Not recorded. Excluded by instruction: automatically subtracting uncertain cashback from the displayed effective price.
- **Consequences**: The offer model must record conditions and certainty. Effective price is shown in two tiers (guaranteed and potential). Offer-calculation tests are required.

## D-007 — Variant-aware product normalization
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Distinguish model, variant, RAM, storage, color, seller, region, warranty and new/refurbished/open-box status. Never compare an 8GB/128GB phone with a 12GB/256GB phone as if identical.
- **Reason**: Stated: comparisons between non-equivalent variants are misleading.
- **Alternatives considered**: Not recorded. Excluded by instruction: comparing non-equivalent variants as identical.
- **Consequences**: A variant identity and equivalence rule is needed before any cross-retailer comparison (OQ-3). Variant-matching and normalization tests are required.

## D-008 — Security boundary and human-controlled checkout
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Never request or store passwords, UPI PINs, card CVVs, OTPs or authentication secrets. No CAPTCHA bypassing. No anti-bot circumvention. Security-sensitive checkout confirmations (CAPTCHA, OTP, payment authorization) stay human-controlled. Checkout automation is a later, browser-assisted workflow only.
- **Reason**: Stated: security.
- **Alternatives considered**: Not recorded. Excluded by instruction: CAPTCHA bypassing, anti-bot circumvention, storing secrets.
- **Consequences**: A blocked or challenged collector degrades (stale or uncertain data, user informed) instead of evading. Automation designs need explicit human hand-off points. *Architect note:* persistent browser sessions raise a question about stored session cookies (OQ-7) that must be settled before any logged-in use.

## D-009 — Two operating modes: Normal and Hunt
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Normal Mode: personalized deal feed, wishlist, price history, discoveries, price/offer/stock changes, recently discovered products, AI explanations. Hunt Mode (major sale events): speed, exact wishlist targets, price and stock changes, variant availability, deal triggers, immediate notifications, minimal UI activity, only actionable events.
- **Reason**: Stated: sale events need speed and clarity.
- **Alternatives considered**: Not recorded.
- **Consequences**: Hunt Mode needs its own priority and polling behavior (OQ-8) and a UI that hides non-actionable activity. The frontend needs a mode switch.

## D-010 — Incremental development workflow and V0.1 scope
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Build incrementally: explain the architecture briefly, build the smallest working version, test, fix, then continue. Preserve working functionality; do not replace working architecture for style. V0.1 covers repository structure, frontend shell, backend shell, database shell, configuration system, premium dashboard UI, health/status endpoint, basic wishlist model and development documentation. No full scraping or checkout automation in V0.1.
- **Reason**: Stated: establish a clean foundation first; the user is a beginner/intermediate developer.
- **Alternatives considered**: Not recorded. Excluded by instruction: generating the whole application in one large response.
- **Consequences**: Work is split into subsystems, each explained first, built minimally and tested. V0.1 contains no scraping or checkout automation.

## D-011 — Vendor-independent Markdown project memory
- **Date**: 2026-09-21
- **Status**: Accepted
- **Decision**: Canonical project context lives as plain Markdown files in `project-memory/`. It depends on no AI vendor's memory feature. No semantic/vector database, no separate SaaS memory service, and no extra dependencies for now.
- **Reason**: Stated: portability and vendor independence, with no proprietary memory system or paid vector database.
- **Alternatives considered**: A semantic/vector database and a separate SaaS memory service were explicitly deferred in the memory-layer brief.
- **Consequences**: Agents must follow `MEMORY_PROTOCOL.md` by hand, so memory can drift from the code; rule 14 (inspect the repository when unsure) is the safeguard. Search tooling can be reconsidered if the memory grows large. The files stay usable with any tool.

## D-012 — Performance principles
- **Date**: 2026-09-21 (recorded)
- **Status**: Accepted
- **Decision**: Async I/O; concurrent collectors where appropriate; persistent browser sessions where appropriate; caching; incremental updates; WebSockets for live dashboard updates; background workers; minimal repeated network requests; efficient database queries; debounced UI updates. Do not relaunch browsers unnecessarily. Do not scan every product when exact product URLs or identifiers are available.
- **Reason**: Stated: performance is a major project requirement, especially in sale events.
- **Alternatives considered**: Not recorded. Excluded by instruction: repeatedly launching browsers; scanning everything when exact identifiers are known.
- **Consequences**: Collectors need scheduling with caching and incremental updates. Browser lifecycle needs managing. UI updates need batching. Hunt Mode depends on all of this (OQ-2, OQ-8).

---

*Entries above this line (D-001 to D-012) were recorded from the Master Project Instructions before any code existed. Entries below were recorded while building the V0.1 implementation itself.*

## D-013 — SQLModel, JSON column for list fields, no migrations yet
- **Date**: 2026-09-26
- **Status**: Accepted
- **Decision**: The backend uses **SQLModel** (combines SQLAlchemy + Pydantic) rather than plain SQLAlchemy + separate Pydantic schemas. One shared `WishlistBase` class defines the fields once; `Wishlist` (the table), `WishlistCreate`, `WishlistUpdate`, and `WishlistRead` each inherit from it and override only what differs. `preferred_brands` (a list of strings) is stored as a JSON column, since SQLite has no native array type — but the JSON column config lives *only* on the `Wishlist` table class, not on the shared base, so it doesn't leak into the non-table schemas. There is no migration tool yet; `SQLModel.metadata.create_all()` creates tables directly from the model classes.
- **Reason**: SQLModel avoids duplicating ~12 fields across four near-identical classes, which is exactly the kind of duplication `MEMORY_PROTOCOL.md`'s spirit and the Master Instructions' "avoid unnecessary abstraction" / "prefer clear code" guidance argue against. A migration tool is real infrastructure that isn't worth adding before there's a second model or real user data to preserve across schema changes.
- **Alternatives considered**: Plain SQLAlchemy with hand-written Pydantic schemas (more boilerplate, rejected for V0.1's scale). Alembic from day one (rejected as premature for a single table with no real data at stake yet — deliberately deferred, see OQ-5 in ARCHITECTURE.md).
- **Consequences**: Schema changes during development are handled by deleting the local `database/bbd_hunter.db` and letting it regenerate — documented in `database/README.md` and code comments. A real migration tool must be introduced before this project has data worth preserving across a schema change.

## D-014 — Wishlist PUT uses partial-update semantics
- **Date**: 2026-09-26
- **Status**: Accepted
- **Decision**: `PUT /api/wishlists/{id}` only changes fields present in the request body; omitted fields keep their existing value. Strict REST convention reserves this behavior for PATCH and has PUT replace the whole resource.
- **Reason**: The V0.1 implementation brief specified `PUT /api/wishlists/{id}` as one of the minimum CRUD endpoints (not PATCH), but a wishlist-editing UI needs "change one field, leave the rest" behavior to be usable. Documented explicitly (in the endpoint's own docstring and here) so the deviation from convention is a visible choice, not a silent bug.
- **Alternatives considered**: Implementing strict PUT-replaces-everything semantics (rejected: would force every future edit request to resend the entire record). Adding a separate PATCH endpoint alongside a strict PUT (rejected as unnecessary duplication for V0.1's scope; can be added later if a real need for strict replace shows up).
- **Consequences**: Anyone integrating with this API from outside this project needs to know PUT here is partial, not a full replace — worth calling out if the API is ever exposed beyond this app's own frontend.

## D-015 — Tests live next to their code, not in a shared root `tests/`
- **Date**: 2026-09-26
- **Status**: Accepted
- **Decision**: Backend tests live in `backend/tests/` (pytest); frontend tests are colocated with their source files under `frontend/src/` (e.g. `App.test.tsx` next to `App.tsx`), the standard Vitest convention. The root `tests/` folder from the V0.1 implementation brief's target tree holds only a README explaining this split, reserved for future cross-system tests.
- **Reason**: Backend tests need to sit inside `backend/` so `app` is importable without installing the project as a package (`backend/pytest.ini` adds that one directory to the import path). Frontend tests colocated with source is how Vitest projects are conventionally organized, and keeps a component and its test easy to find together. A literal root `tests/` folder would otherwise sit empty, which the V0.1 brief itself says to avoid ("do not create unnecessary empty files just to match this tree").
- **Alternatives considered**: A literal root `tests/` folder holding all tests for both frontend and backend (rejected: breaks the natural import/tooling setup for both pytest and Vitest, for no real benefit).
- **Consequences**: Someone looking for "all the tests" needs to know to check two locations, not one — mitigated by `tests/README.md` pointing to both, and by this decision record.

## D-016 — Conservative frontend dependency choices given no network access to verify them
- **Date**: 2026-09-26
- **Status**: Accepted
- **Decision**: The frontend uses **Tailwind CSS v3** (PostCSS-based config) rather than v4 (CSS-first config, different plugin architecture), and does **not** include Framer Motion as a V0.1 dependency, relying on Tailwind transitions and a couple of CSS keyframes for the dashboard's few subtle animations instead.
- **Reason**: This code was written in a sandboxed environment with no network access (confirmed: both `pip` and `npm` registry requests failed), so no dependency's exact current API could be verified by actually installing and running it. Tailwind v3's setup is long-established and well-understood; a mistake in recalling Tailwind v4's newer API would break the entire frontend build, which is a worse failure mode than "using an older but definitely-correct major version." The V0.1 implementation brief itself only lists "Tailwind CSS if practical" and "Lucide icons if practical," without mentioning Framer Motion, and V0.1's dashboard doesn't yet have complex animation choreography (like Hunt Mode transitions) that would clearly justify the added dependency.
- **Alternatives considered**: Tailwind v4 (rejected for this reason: higher risk of an unverifiable, build-breaking mistake, for a version-number benefit that doesn't matter functionally yet). Including Framer Motion anyway, matching the original Master Instructions' stack list (rejected for V0.1 specifically, as an unnecessary dependency for what the dashboard currently needs; trivial to add later).
- **Consequences**: The frontend is on an older major Tailwind version than may be "current" by the time this is read; upgrading later is a normal, well-documented migration, not a rewrite. If a future version's motion needs grow past what CSS transitions/keyframes comfortably express, add Framer Motion then rather than now.

## D-017 — V0.1 visual design system: warm charcoal + amber, not the generic dark-mode default
- **Date**: 2026-09-26
- **Status**: Accepted
- **Decision**: The dashboard uses a warm dark charcoal background (not pure/blue-black), **amber/gold** as the single primary interactive accent, and two additional colors used *only* for functional price-signal meaning (a muted green for positive/price-drop, a muted rust for negative/price-rise) — never as decoration. Typography is IBM Plex Sans for UI text and IBM Plex Mono reserved specifically for numeric data (prices, specs), never for decorative labels.
- **Reason**: A near-black background with a single bright green or vermilion accent is one of the most common AI-generated-design patterns, called out explicitly as a cliché to avoid. Amber was chosen instead as a deliberate reference to real trading-terminal visual heritage (Bloomberg Terminal's black-and-amber displays), which the brief's own words ("stock-trading terminal") justify directly, rather than an arbitrary color choice — and separately, gold/amber carries a "value" association relevant to a deal-hunting tool.
- **Alternatives considered**: The near-black + green/vermilion pattern initially drafted, then deliberately rejected once recognized as the common generic default. A cooler blue/teal "HUD" palette was also considered and set aside in favor of the more specifically-grounded amber-terminal reference.
- **Consequences**: Every new UI surface added later should route color choices through the same three-color functional system (`tailwind.config.js`'s `signal.amber` / `signal.positive` / `signal.negative`) rather than introducing new decorative colors, to keep the "restraint, one bold element" principle intact as the dashboard grows.

---

## Template for new entries (append below this line)
```
## D-### — short title
- **Date**: YYYY-MM-DD
- **Status**: Accepted / Proposed / Superseded by D-###
- **Decision**: what was decided
- **Reason**: why
- **Alternatives considered**: what else was weighed, or "Not recorded"
- **Consequences**: what follows, including costs and risks
```