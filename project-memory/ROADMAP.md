# BBD HUNTER — Roadmap

> Purpose: planned development phases. Near-term work is kept separate from future ideas.
> Last updated: 2026-09-29 · Memory layer V0.1
> **V0.1 and V0.2 are defined by the user (done).** Phases after V0.2 are a **draft ordering** derived from the Master Instructions and need the user's approval (TODO T-040) — see the note on V0.3 below in particular, which offers a choice rather than presupposing one.

## Principles for sequencing
- Foundation first; then data and price logic; then live collection; then AI; then Hunt Mode and notifications. (Draft.)
- Each phase follows the workflow in D-010: brief architecture note, smallest working version, tests, fixes, next.
- Preserve working functionality. Never replace working architecture for style.

## Done

### V0.1 — Foundation (defined by the user)
- **Scope**: repository structure · frontend shell · backend shell · database shell · configuration system · premium dashboard UI · health/status endpoint · basic wishlist model · development documentation.
- **Status**: `[VERIFIED]` — user-confirmed running (2026-09-29). 18 backend + 8 frontend tests.

### V0.2 — Product & Deal Data Foundation (defined by the user)
- **Scope**: the full product/deal data model (Retailer, Product, ProductVariant, RetailerListing, PriceObservation, Offer) with real constraints; deterministic deal assessment; deterministic product-name normalization; API endpoints for all of it; a frontend Data Explorer; optional clearly-labelled demo data; tests. *(This single phase turned out to cover what an earlier draft of this roadmap had split across two future phases — see the git-free note in `CHANGELOG.md`'s 2026-09-29 entry for exactly what was built.)*
- **Out of scope**: retailer scraping, AI/Ollama integration, checkout/CAPTCHA/OTP/payment automation. None were built — confirmed true.
- **Status**: `[BUILT]`, 2026-09-29 — written and passed offline static checks, not yet confirmed by an actual run (same situation V0.1 was in before it was verified; see `CURRENT_STATE.md`). Running it for real is TODO T-005, the top open item right now.
- **Acceptance criteria** (status 2026-10-01: automated criteria **met in a Linux sandbox** — `pytest` 115 passed, `npm test` 14 passed, `npm run build` succeeded; still to confirm on Windows and in a real browser, T-005): `pytest` passes all backend tests (115); `npm test` passes all 14 frontend tests; the Data Explorer loads and, after running the optional seed script, shows a browsable product → variants → listings → history/offers/deal-signals drill-down with no fabricated data anywhere; the six named deal-engine scenarios behave as documented.

## Next — needs the user's decision (TODO T-040)

Three reasonable directions exist from here, each unlocking something different. This roadmap doesn't presuppose which one is V0.3 — that's an open choice, not a default:

### Option A — First retailer collector
Real data flowing in for the first time, rather than manual/demo entry. Needs the retailer research first (`KNOWLEDGE/retailers.md`, RQ-02, RQ-03 — terms of service and robots.txt review), plus OQ-2 (scheduling) and OQ-7 (session handling without storing secrets) decided. Highest-value for making the app actually useful day to day; also the riskiest (external dependencies, a live site's behavior to handle gracefully).

### Option B — AI layer
Provider abstraction with an Ollama-compatible provider; natural-language wishlist parsing (FR-101) with schema validation; explanations of why a deal matches (extending FR-133 beyond budget-only); review analysis. Highest-value for the "AI shopping intelligence" part of the product vision; doesn't need real collected data to be useful (works fine against demo/manually-entered data).

### Option C — Wishlist-to-product matching (finish OQ-3 / T-062)
Link a wishlist entry to specific products/variants it's shopping for, and let the deal engine scan for matches automatically instead of taking an ad hoc `wishlist_id` per request. Unlocks FR-160/161 (discovery, change tracking) and is a prerequisite for a real "personalized deal feed" (FR-170). Smaller in scope than A or B; a reasonable "finish what V0.2 started" option.

## Later (draft, unaffected by which option above comes first)

### Notifications and Hunt Mode
Notification delivery; Hunt Mode (speed, exact targets, stock/variant triggers, immediate alerts, minimal UI). Needs OQ-6 and OQ-8, and realistically needs at least one of Options A/B/C done first (nothing to notify about without real data, matching, or both).

### WebSocket live updates
Replace V0.1's 15-second polling with pushed updates once there's something worth pushing (a live collector or a background matching process).

## Future ideas (unscheduled)
- More retailers (Amazon, Croma, Reliance, Vijay Sales, generic adapter).
- Review analysis and recurring-complaint detection.
- Suspicious or inconsistent listing detection.
- Discovery of unwishlisted deals and alternative products.
- Spec normalization across manufacturers using authoritative sources.
- Browser-assisted checkout with human-controlled security steps (very late; see D-008).
- Expansion beyond smartphones and India (implied by "initially"; nothing is planned).
