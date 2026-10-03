# BBD HUNTER — Requirements

> Purpose: functional and non-functional requirements, separated into implemented / planned / experimental / explicitly out of scope.
> Last updated: 2026-10-01 · Memory layer V0.1
> Source: the Master Project Instructions, the Project Memory Layer V0.1 brief, the V0.1 implementation brief, and the V0.2 (Product & Deal Data Foundation) brief. The split into "planned" vs "experimental" is a **proposed classification** (the user has not labelled anything experimental) — confirm or change it.

Status tags: `[VERIFIED]` confirmed by actually running it · `[BUILT]` written and passed offline static checks but not yet run live · `[PLANNED]` intended, not built · `[PARTIAL]` some of the requirement is built, some isn't — see the note · `[UNVERIFIED]` believed, not checked · `[UNKNOWN]` no information (see `MEMORY_PROTOCOL.md`).

## 1. Implemented
### V0.1 scope — `[VERIFIED]` (user-confirmed running, 2026-09-29)
| ID | Requirement | Where |
|---|---|---|
| R-V01-1 | Repository structure | see `ARCHITECTURE.md` §12 for the real tree |
| R-V01-2 | Frontend shell | `frontend/` |
| R-V01-3 | Backend shell | `backend/app/main.py` |
| R-V01-4 | Database shell | `backend/app/database.py`, `database/` |
| R-V01-5 | Configuration system (environment variables, `.env.example`) | `backend/app/config.py`, `backend/.env.example`, `frontend/.env.example` |
| R-V01-6 | Premium dashboard UI | `frontend/src/App.tsx` and `frontend/src/components/`; design reasoning in D-017 |
| R-V01-7 | Health/status endpoint | `backend/app/routers/health.py` — a real DB check, not hardcoded |
| R-V01-8 | Basic wishlist model | `backend/app/models/wishlist.py`, more than "basic" (full CRUD) |
| R-V01-9 | Development documentation | root `README.md` |

Implemented outside the application: `project-memory/` (this memory layer), first created 2026-09-21, updated 2026-09-26 and 2026-09-29.

## 2. Planned

### 2.1 V0.2 scope (defined by the user) — `[VERIFIED]` by a real test run on 2026-10-01 (Linux sandbox; Windows re-run pending, T-005)
| ID | Requirement | Status | Where |
|---|---|---|---|
| R-V02-1 | Core domain model (Retailer, Product, ProductVariant, RetailerListing, PriceObservation, Offer) | `[VERIFIED]` | `backend/app/models/` |
| R-V02-2 | Deterministic deal assessment | `[VERIFIED]` | `backend/app/deal_engine/` |
| R-V02-3 | Deterministic product-name normalization | `[VERIFIED]` | `backend/app/normalization.py` |
| R-V02-4 | API endpoints for all six new entities + deal assessment | `[VERIFIED]` | `backend/app/routers/` |
| R-V02-5 | Frontend Data Explorer | `[VERIFIED]` (jsdom tests + build; not yet browser-tested) | `frontend/src/components/explorer/` |
| R-V02-6 | Optional, clearly-labelled demo/fixture data | `[VERIFIED]` | `backend/scripts/seed_demo_data.py` |
| R-V02-7 | Tests (database/model, normalization, deal engine, API) | `[VERIFIED]` | `backend/tests/` — 115 total, all passing (18 V0.1 + 81 V0.2 + 16 regression) |
| R-V02-8 | Preserve all existing V0.1 functionality and tests | `[VERIFIED]` — all V0.1 tests pass | every V0.1 file except the 4 deliberately touched (see `CHANGELOG.md`) |

Not in V0.2: retailer scraping, AI/Ollama integration, checkout/CAPTCHA/OTP/payment automation. None were implemented — confirmed true.

### 2.2 Functional requirements (phase TBD unless stated)

**Understanding requirements**
- FR-101 `[PLANNED]` Convert natural-language requirements into structured preferences (budget target and maximum, minimum storage, RAM preference, camera / gaming / battery priority, wireless-charging preference, software preference, brand preference). *(V0.1's wishlist form does this manually, by the human typing into structured fields -- no AI parsing exists yet.)*
- FR-102 `[PARTIAL]` Validate AI output against a schema before use — n/a yet, no AI output exists. Enforce explicit constraints in a deterministic rule engine — `[BUILT]` for one listing at a time, on request (`app/deal_engine/assess_deal`, checked against an explicitly-passed wishlist's budget), `[PLANNED]` as an automated scan of the whole database against a wishlist's full constraint set (storage, variant, availability, seller conditions aren't checked by the deal engine yet, only budget — see T-062).

**Collection and discovery**
- FR-110 `[PLANNED]` Discover relevant smartphones across Indian retailers. No collectors exist.
- FR-111 `[PLANNED]` One collector adapter per retailer, normalizing to a common schema. The common schema now exists (`app/models/`) for a collector to target; no collector exists yet.
- FR-112 `[PLANNED]` Prefer exact product URLs and identifiers over broad scans. N/A without a collector.

**Price intelligence**
- FR-120 `[BUILT]` Store observations: product, variant, seller, retailer, price, MRP (if available), timestamp, availability, relevant offer information. → `PriceObservation` + `RetailerListing` (seller/availability live on the listing, which every observation is scoped to).
- FR-121 `[PARTIAL]` Current, lowest, highest and average price — `[BUILT]`. Recent average, 7/30/90-day lows, percentage change, and distance from historical low — `[PLANNED]` (OQ-4 in `ARCHITECTURE.md`; V0.2's `price_dropped_from_previous_observation` and `lowest_observed_in_history` cover "better/worse than before" without these specific windowed metrics).
- FR-122 `[BUILT]` Detect genuine price drops and record lows, with the exact required wording. Tested in `test_deal_engine.py::test_never_claims_all_time_low_wording`.
- FR-123 `[BUILT]` MRP discount is surfaced as a caveat only, never as evidence. Tested in `test_mrp_discount_alone_is_labelled_a_caveat_not_a_reason`.

**Deal engine**
- FR-130 `[BUILT]` Separate base price, guaranteed discount, conditional discount and cashback. → `DealAssessment`'s four separate totals.
- FR-131 `[BUILT]` "Potential effective price" shown only when meaningful; cashback never auto-subtracted, even when the cashback offer itself is guaranteed. Tested in `test_cashback_is_never_netted_into_effective_price`.
- FR-132 `[BUILT]` `Offer.is_guaranteed` classifies every offer.
- FR-133 `[PARTIAL]` The deal engine explains its signals in plain language (`reasons`/`caveats`), and checks wishlist budget specifically when given a `wishlist_id` — `[BUILT]` for that scope. Matching against the *rest* of a wishlist's preferences (camera/gaming/battery priority, storage minimum, brand, software) is `[PLANNED]` — not yet part of the deal engine's inputs.

**Product normalization and phone intelligence**
- FR-140 `[PARTIAL]` Model, variant, RAM, storage, color, seller — `[BUILT]`. Region, warranty, and new/refurbished/open-box status — `[PLANNED]`, not yet fields on `ProductVariant` (T-061).
- FR-141 `[BUILT]` Tested explicitly in `test_different_configs_do_not_collapse_into_one_variant`.
- FR-142 `[PLANNED]` Track phone specifications (SoC, display, camera, etc.) — not part of V0.2; `Product.description` is free text only.
- FR-143 `[PARTIAL]` `app/normalization.py` normalizes product *names/titles* into brand/RAM/storage/color — `[BUILT]`, deliberately basic (pattern matching, not fuzzy/semantic — see its own docstring). Normalizing *specifications* between manufacturers (e.g. reconciling how two brands describe the same charging speed) is a different, larger task and is `[PLANNED]`.

**Wishlist, changes and notifications**
- FR-160 `[PARTIAL]` Wishlist of *preferences* with deterministic conditions — `[BUILT]` since V0.1. Wishlist of *exact targets* (linked to a specific Product/ProductVariant) — `[PLANNED]`, still open (OQ-3's matching question, T-062).
- FR-161 `[PLANNED]` Track price, offer and stock changes and newly discovered products *over time*. V0.2's Data Explorer shows current state and full price history on request, but nothing watches for and records *changes* as events yet — no events/notifications system exists.
- FR-162 `[PLANNED]` Notify the user when configured conditions are met. No notification delivery exists.

**Modes and UI**
- FR-170 `[PARTIAL]` Wishlist, price history (Data Explorer, browsed manually) — `[BUILT]`. Personalized deal feed, discoveries, price/offer/stock *change* tracking, AI explanations — `[PLANNED]`.
- FR-171 `[PLANNED]` Hunt Mode. No UI for it exists.
- FR-172 `[PLANNED]` Live dashboard updates over WebSockets. V0.1's health check still polls every 15s; V0.2's Data Explorer is fetch-on-navigation, not live-updating.

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
