# Retailers and Collectors

> Purpose: retailer-specific knowledge and collector design considerations.
> Last updated: 2026-09-21 · Memory layer V0.1

## Status
**No retailer-specific technical knowledge has been verified.** Page structure, data endpoints, offer presentation, rate limits and terms of service are all `[UNKNOWN]`. Record findings here, with source and date, as they are learned.

## Retailer registry
| Retailer | Planned collector | Data-access method | Terms/robots reviewed | Status |
|---|---|---|---|---|
| Flipkart | `collectors/flipkart` | `[UNKNOWN]` | `[UNKNOWN]` | `[PLANNED]`; Big Billion Days is the motivating event |
| Amazon | `collectors/amazon` | `[UNKNOWN]` | `[UNKNOWN]` | `[PLANNED]` |
| Croma | `collectors/croma` | `[UNKNOWN]` | `[UNKNOWN]` | `[PLANNED]` |
| Reliance | `collectors/reliance` | `[UNKNOWN]` | `[UNKNOWN]` | `[PLANNED]` |
| Vijay Sales | `collectors/vijaysales` | `[UNKNOWN]` | `[UNKNOWN]` | `[PLANNED]` |
| Generic | `collectors/generic` | `[UNKNOWN]` | n/a | `[PLANNED]` |

Which retailer comes first is `[UNKNOWN]` (not decided). No collector is in V0.1.

## Design requirements *[source: Master]*
- One adapter per retailer. Collector code is isolated; no other component depends on a retailer's HTML structure (D-004).
- Every collector outputs the common schema: product, variant, seller, retailer, price, MRP (if available), timestamp, availability, relevant offer information.
- Prefer exact product URLs or identifiers. Do not scan every possible product when they are available.
- Async I/O; concurrent collectors where appropriate; persistent browser sessions where appropriate; do not launch browsers repeatedly; cache; update incrementally; minimize repeated requests (D-012).
- No CAPTCHA bypassing. No anti-bot circumvention (D-008).

## Collector contract additions *[draft, proposed 2026-09-21, needs approval]*
- Include the source URL and the collection time with each observation.
- Report parse problems as warnings on the observation instead of guessing a value. A missing or unparseable field is "unknown", never a default.
- Return offers with their conditions and a guaranteed-vs-conditional marker, or "unknown" if the page does not make that clear.
- Never write to the database directly; hand validated results to the core.

## When a retailer blocks or challenges a collector
Do not evade. Mark the affected data as stale or uncertain, back off, and tell the user. If a CAPTCHA or verification appears, it is a human step.

## Before building any collector *[architect note, added 2026-09-21]*
Review that retailer's terms of service and robots.txt, and check whether an official or affiliate data source exists (RQ-02). Record the outcome in the registry above.

## Seller and listing considerations
- The same model can appear from multiple sellers with different prices, warranty and condition. Record seller and condition for every observation (D-007).
- New, refurbished and open-box listings are not comparable to each other.
- Regional and warranty differences must be captured when visible. How each retailer presents them is `[UNKNOWN]`.

## Retailer findings log
None yet. Use the finding format in `research.md`.
