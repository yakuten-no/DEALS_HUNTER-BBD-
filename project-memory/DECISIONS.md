# BBD HUNTER — Decision Log

> Purpose: append-only history of architectural and product decisions. Never edit or delete an old entry. To change a decision, add a new entry at the bottom and mark the old one "Superseded by D-###".
> Last updated: 2026-09-21 · Memory layer V0.1

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