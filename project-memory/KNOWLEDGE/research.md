# Research Notes

> Purpose: useful external technical and product findings for BBD HUNTER, with sources.
> Last updated: 2026-09-21 · Memory layer V0.1

## Status
**No research findings recorded yet.** Nothing in this file has been checked against external sources. The entries below are open questions, not findings. Do not treat any of them as facts.

## How to record a finding
Copy this block into "Findings" (newest first):
```
### F-### — topic
- Date: YYYY-MM-DD
- Source: URL or document name (no secrets, no pasted page dumps)
- Finding: 1-3 sentences in your own words
- Confidence: high / medium / low, and why
- Implication for BBD HUNTER: what to do or decide
- Related: RQ-##, D-###, files
```

## Findings
None.

## Open research questions
Priority: P1 needed before the phase shown; P2 useful; P3 later.

| ID | Question | Why it matters | Needed by | Priority |
|---|---|---|---|---|
| RQ-01 | When is the next Flipkart Big Billion Days, and which other major Indian sale events matter for smartphones? | Sets the target date for Hunt Mode readiness | Planning | P1 |
| RQ-02 | For each target retailer, what legitimate ways exist to obtain price and stock data (official or affiliate feeds/APIs, public pages), and what do the terms of service and robots.txt allow? | Decides whether and how a collector can be built without circumvention (D-008) | V0.4 | P1 |
| RQ-03 | How does each retailer present offers (bank/card, exchange, coupons, EMI, membership), and which are guaranteed vs conditional? | Needed for D-006 | V0.3-V0.4 | P1 |
| RQ-04 | How can a "genuine discount" be judged when price history is short (cold start)? Is any legitimate historical source available, or must history simply accumulate? | D-005 forbids unsupported claims | V0.2-V0.3 | P1 |
| RQ-05 | Which Ollama-compatible local models run acceptably on the owner's Windows PC (hardware `[UNKNOWN]`) for structured-output extraction and review summarization, and how reliably do they produce schema-valid output? | Feasibility of the AI layer (D-001, D-003) | V0.5 | P2 |
| RQ-06 | Expected SQLite write volume during Hunt Mode; need for WAL mode; migration tooling choice | OQ-2, OQ-5 | V0.2-V0.4 | P2 |
| RQ-07 | How do Playwright persistent sessions behave on Windows, and how can they be used without storing authentication secrets? | OQ-7, D-008 | V0.4 | P2 |
| RQ-08 | Which notification channels work well on a local Windows setup? | OQ-6 | V0.6 | P2 |
| RQ-09 | Which authoritative sources exist for phone specifications, and what are their licensing terms? | See `phone-data.md` | V0.2 | P2 |
