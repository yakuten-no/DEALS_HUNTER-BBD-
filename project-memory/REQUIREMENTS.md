# BBD HUNTER — Requirements

> Purpose: functional and non-functional requirements, separated into implemented / planned / experimental / explicitly out of scope.
> Last updated: 2026-09-21 · Memory layer V0.1
> Source: the Master Project Instructions and the Project Memory Layer V0.1 brief. The split into "planned" vs "experimental" is a **proposed classification** (the user has not labelled anything experimental) — confirm or change it.

Status tags: `[VERIFIED]` `[PLANNED]` `[UNVERIFIED]` `[UNKNOWN]` (see `MEMORY_PROTOCOL.md`).

## 1. Implemented
**None verified.** No application code was available to inspect on 2026-09-21. When the repository is inspected, move confirmed items here with a pointer to the implementing file and its tests.

Implemented outside the application: `project-memory/` (this memory layer), 2026-09-21.

## 2. Planned

### 2.1 V0.1 scope (defined by the user)
| ID | Requirement | Status |
|---|---|---|
| R-V01-1 | Repository structure | `[UNVERIFIED]` |
| R-V01-2 | Frontend shell | `[UNVERIFIED]` |
| R-V01-3 | Backend shell | `[UNVERIFIED]` |
| R-V01-4 | Database shell | `[UNVERIFIED]` |
| R-V01-5 | Configuration system (environment variables, `.env.example`) | `[UNVERIFIED]` |
| R-V01-6 | Premium dashboard UI | `[UNVERIFIED]` |
| R-V01-7 | Health/status endpoint | `[UNVERIFIED]` |
| R-V01-8 | Basic wishlist model | `[UNVERIFIED]` |
| R-V01-9 | Development documentation | `[UNVERIFIED]` |

Not in V0.1: full scraping, checkout automation.

### 2.2 Functional requirements (phase TBD unless stated)

**Understanding requirements**
- FR-101 Convert natural-language requirements into structured preferences (budget target and maximum, minimum storage, RAM preference, camera / gaming / battery priority, wireless-charging preference, software preference, brand preference).
- FR-102 Validate AI output against a schema before use. Enforce explicit constraints (maximum price, minimum storage, required variant, availability, seller conditions) in a deterministic rule engine.

**Collection and discovery**
- FR-110 Discover relevant smartphones across Indian retailers (Flipkart, Amazon, Croma, Reliance, Vijay Sales, generic).
- FR-111 One collector adapter per retailer, normalizing to a common schema, isolated from the rest of the app.
- FR-112 Prefer exact product URLs and identifiers over broad scans.

**Price intelligence**
- FR-120 Store observations: product, variant, seller, retailer, price, MRP (if available), timestamp, availability, relevant offer information.
- FR-121 Calculate current, lowest, highest and average price, recent average, 7/30/90-day lows, percentage change, and distance from historical low.
- FR-122 Detect genuine price drops and record lows. Claim "all-time low" only when stored history supports it; otherwise say "lowest observed in our history".
- FR-123 Never treat an advertised MRP discount as proof of a genuine deal.

**Deal engine**
- FR-130 Separate base price, guaranteed discount, conditional discount and cashback.
- FR-131 Show "Potential effective price" when conditions are not guaranteed. Never auto-subtract uncertain cashback.
- FR-132 Identify available discounts and offers, and classify each as guaranteed or conditional.
- FR-133 Explain why a deal matches the user's preferences (an explanation layered on a deterministic result).

**Product normalization and phone intelligence**
- FR-140 Distinguish model, variant, RAM, storage, color, seller, region, warranty and new/refurbished/open-box status.
- FR-141 Never compare non-equivalent variants (for example 8GB/128GB vs 12GB/256GB) as identical.
- FR-142 Track phone specifications where available (field list in `KNOWLEDGE/phone-data.md`).
- FR-143 Normalize specifications between manufacturers.

**Wishlist, changes and notifications**
- FR-160 Wishlist of exact targets with deterministic conditions.
- FR-161 Track price, offer and stock changes and newly discovered products.
- FR-162 Notify the user when configured conditions are met.

**Modes and UI**
- FR-170 Normal Mode: personalized deal feed, wishlist, price history, discoveries, price/offer/stock changes, recently discovered products, AI explanations.
- FR-171 Hunt Mode: speed; exact wishlist targets; price, stock and variant-availability changes; deal triggers; immediate notifications; minimal UI activity; only actionable events.
- FR-172 Live dashboard updates over WebSockets.

### 2.3 Non-functional requirements
- NFR-01 Local-first: runs on a Windows PC with no paid cloud backend; external services optional.
- NFR-02 No dependence on a paid AI API; AI sits behind a provider abstraction (Ollama-compatible first).
- NFR-03 Performance: async I/O, concurrent collectors where appropriate, persistent browser sessions where appropriate, caching, incremental updates, background workers, minimal repeated network requests, efficient queries, debounced UI updates; no unnecessary browser launches.
- NFR-04 Data honesty: never invent prices, discounts, specs, availability or offers; mark uncertainty; keep calculations transparent.
- NFR-05 Security: never request or store passwords, UPI PINs, card CVVs, OTPs or authentication secrets; security-sensitive checkout confirmation stays human-controlled.
- NFR-06 Modularity: components separated as in `ARCHITECTURE.md`; collector code isolated.
- NFR-07 Code quality: production-quality but understandable; TypeScript types; Python type hints; configuration via environment variables; `.env.example`; comments only where they clarify non-obvious logic; avoid unnecessary abstraction.
- NFR-08 Testing: tests for price parsing, currency parsing, variant matching, product normalization, offer calculations, price-history calculations, deal detection, wishlist matching, and AI structured-output validation.
- NFR-09 UX: fast, premium, modern, minimal, information-dense without clutter; a clean futuristic look (not a generic admin dashboard); subtle animation; excellent typography; excellent on desktop; responsive; extremely clear during sale events.
- NFR-10 Portability: the project can be copied from the browser-based development environment to a Windows PC and run; exact install commands are documented; no dependency is assumed to be installed.
- NFR-11 Incremental delivery: small working increments; working functionality is preserved.

## 3. Experimental
These depend on unproven techniques (local-model quality), uncertain data access, or high risk. Classification proposed on 2026-09-21.
- EX-01 Discover deals the user did not add to the wishlist, matched to their preferences.
- EX-02 Summarize reviews and identify recurring complaints.
- EX-03 Detect suspicious or inconsistent listing information.
- EX-04 Suggest alternative products; explain price-history context in words.
- EX-05 Browser-assisted checkout workflows. CAPTCHA, OTP, payment authorization and other security-sensitive confirmations remain human-controlled. Late-stage; not before the core is proven.

## 4. Explicitly out of scope
- OOS-01 CAPTCHA bypassing.
- OOS-02 Anti-bot circumvention.
- OOS-03 Requesting or storing passwords, UPI PINs, card CVVs, OTPs or authentication secrets.
- OOS-04 Letting an LLM decide financial actions from free-form reasoning alone.
- OOS-05 Autonomous completion of security-sensitive checkout steps.
- OOS-06 Requiring a paid cloud backend or a paid AI API.
- OOS-07 Full scraping and checkout automation **in V0.1**.
- OOS-08 Copying Nothing's proprietary design (inspiration from its visual simplicity only).
- OOS-09 For the memory layer (for now): a semantic/vector database, a separate SaaS memory service, and extra dependencies.