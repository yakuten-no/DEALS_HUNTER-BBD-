# collectors/

Still empty by design -- this task explicitly excludes retailer scraping
(see project-memory/DECISIONS.md, D-010, and the V0.2 brief's own "DO NOT
implement retailer scraping in V0.2" instruction).

## What will live here

One adapter per retailer (for example `flipkart/`, `amazon/`, `croma/`,
`reliance/`, `vijaysales/`, `generic/`), each normalizing its output into
the common schema that now exists in `backend/app/models/` (V0.2):
`Retailer`, `Product`, `ProductVariant`, `RetailerListing`,
`PriceObservation`, `Offer`. Collector code stays isolated here so no
other part of the app depends on any one retailer's HTML structure (D-004
in project-memory/DECISIONS.md).

The intended pipeline a collector feeds into (conceptual, from the V0.2
brief):
```
Collector -> Raw Listing -> Normalizer -> Product Matcher -> RetailerListing -> PriceObservation -> Offer -> Deal Engine
```
`backend/app/normalization.py` (deterministic product-name parsing) and
`backend/app/deal_engine/` (deterministic deal assessment) already exist
and are ready for a collector to feed into -- a collector's job is only to
turn one retailer's page into a raw listing; normalization and deal
assessment are already handled downstream of that.

## Before building the first collector

Read `project-memory/KNOWLEDGE/retailers.md` and `research.md` (open
question RQ-02): each retailer's terms of service and `robots.txt` need
reviewing, and no CAPTCHA bypassing or anti-bot circumvention is allowed
(D-008).
