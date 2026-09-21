# Phone Data and Intelligence

> Purpose: what normalized phone/product intelligence BBD HUNTER needs, and which data sources are known.
> Last updated: 2026-09-21 · Memory layer V0.1

## Status
Requirements come from the Master Instructions. **No data source has been selected or verified**, and no schema exists yet. Field representations below are suggestions *[draft]*.

## Product identity dimensions
Model · variant · RAM · storage · color · seller · region · warranty · new/refurbished/open-box status.

Rule: never compare an 8GB/128GB phone with a 12GB/256GB phone as if identical (D-007). Which of these dimensions make two listings "the same comparable variant" is undecided (OQ-3). Proposal: model + RAM + storage + condition + region as the key, with color, seller and warranty as attributes.

## Specification fields to track (where available)
| Group | Fields | Suggested representation *[draft]* |
|---|---|---|
| Processor | SoC, CPU, GPU | Normalized vendor and model names |
| Memory | RAM; storage; storage technology | RAM and storage in GB (integers); technology as a controlled vocabulary |
| Display | Display; refresh rate; resolution | Panel description; Hz; pixels |
| Battery and charging | Battery; wired charging; wireless charging | mAh; watts; wireless as yes / no / unknown |
| Durability | IP rating | Standard IP code, or unknown |
| Cameras | Main; ultrawide; telephoto/periscope; OIS; video capabilities; front | MP and lens presence per camera; OIS yes / no / unknown; video modes as a list |
| Software | Software version; software support period | OS or skin version; years of OS and security updates |
| Connectivity | Connectivity features | A list; vocabulary to be defined |

## Rules for spec data
- Every value carries its source and a certainty marker. Unknown is not false: "wireless charging: unknown" must not be shown as "no" (D-005). *[source: Master, uncertainty rule]*
- Normalize units (GB/TB, mAh, W, Hz, MP, inches) and names (SoC and brand spelling) so phones from different manufacturers compare fairly. *[source: Master, normalization goal]*
- Do not guess a missing spec. If sources disagree, keep both values and flag the conflict; prefer the manufacturer's own specification. *[draft]*
- Listing text that contradicts the normalized spec sheet is a signal for the "suspicious or inconsistent listing" check (EX-03, experimental).

## Preference fields the specs must support (from the user's requirements)
Budget target and maximum · minimum storage · RAM preference · camera priority · gaming priority · battery priority · wireless-charging preference · software preference (for example a liking for Nothing OS) · brand preference.

## Known data sources
**None selected or verified.** Candidate source types, not yet evaluated for access or licensing: retailer product pages, manufacturer specification pages, third-party specification databases. Evaluate under RQ-09 before use, and record the outcome in `research.md`.

## Open questions
- Which authoritative source(s) supply specs, and under what terms (RQ-09)?
- How to map retailer-listed variants and SKUs to canonical models and variants?
- Controlled vocabularies for storage technology and connectivity.
- How to represent software support periods that manufacturers state differently.
