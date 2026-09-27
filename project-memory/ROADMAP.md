# BBD HUNTER — Roadmap

> Purpose: planned development phases. Near-term work is kept separate from future ideas.
> Last updated: 2026-09-26 · Memory layer V0.1
> Only **V0.1** is defined by the user. Phases after V0.1 are a **draft ordering** derived from the Master Instructions and need the user's approval (TODO T-040).

## Principles for sequencing
- Foundation first; then data and price logic; then live collection; then AI; then Hunt Mode and notifications. (Draft.)
- Each phase follows the workflow in D-010: brief architecture note, smallest working version, tests, fixes, next.
- Preserve working functionality. Never replace working architecture for style.

## Now

### V0.1 — Foundation (defined by the user)
- **Scope**: repository structure · frontend shell · backend shell · database shell · configuration system · premium dashboard UI · health/status endpoint · basic wishlist model · development documentation.
- **Out of scope**: full scraping, checkout automation. Neither was built — confirmed true.
- **Status**: `[BUILT]`, 2026-09-26 — written and passed offline static checks, but not yet confirmed by an actual run (no network access in the build environment; see `CURRENT_STATE.md`). Running it for real is TODO T-003, the top open item right now.
- **Acceptance criteria** (updated from "proposed" now that the scope is built; still to be *confirmed*, not yet confirmed): frontend and backend start with documented commands (Windows and macOS/Linux both given in the root `README.md`); the health/status endpoint responds with a real database check; a wishlist item can be created and persisted in SQLite; `.env.example` files exist for both backend and frontend and no secrets are committed; the dashboard renders with a working hunt input, wishlist panel, live system status, honest empty deal feed, and activity log; 18 backend + 8 frontend tests exist and are expected to pass once actually run.

## Next (draft, not yet approved)

### V0.2 — Data model and price-intelligence core
Product / variant / seller / retailer / listing / observation / offer schema; price and currency parsing; variant matching and normalization; price-history metrics (current, lowest, highest, average, recent average, 7/30/90-day lows, percentage change, distance from low); tests. Data comes from fixtures or manual entry, with no live collectors yet. Decisions needed: variant identity key (OQ-3), "recent average" window (OQ-4), migration approach (OQ-5).

### V0.3 — Deal engine and rule engine
Base / guaranteed / conditional / cashback separation; potential effective price; deterministic wishlist rules (maximum price, minimum storage, required variant, availability, seller conditions); genuine-drop and record-low detection with honest wording; tests.

## Later (draft)

### V0.4 — First collector and live updates
First retailer adapter writing to the common schema; background worker and scheduling; WebSocket live updates; persistent browser-session handling. Needs the retailer research first (`KNOWLEDGE/retailers.md`), including terms of service and the no-circumvention rule, plus OQ-2 and OQ-7.

### V0.5 — AI layer
Provider abstraction with an Ollama-compatible provider; natural language to structured preferences with schema validation; explanations of why a deal matches; AI output-validation tests.

### V0.6 — Notifications and Hunt Mode
Notification delivery; Hunt Mode (speed, exact targets, stock/variant triggers, immediate alerts, minimal UI). Needs OQ-6 and OQ-8.

## Future ideas (unscheduled)
- More retailers (Amazon, Croma, Reliance, Vijay Sales, generic adapter).
- Review analysis and recurring-complaint detection.
- Suspicious or inconsistent listing detection.
- Discovery of unwishlisted deals and alternative products.
- Spec normalization across manufacturers using authoritative sources.
- Browser-assisted checkout with human-controlled security steps (very late; see D-008).
- Expansion beyond smartphones and India (implied by "initially"; nothing is planned).
