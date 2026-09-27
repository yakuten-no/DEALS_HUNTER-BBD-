# collectors/

Empty in V0.1 by design -- this task explicitly excludes retailer scraping
(see project-memory/DECISIONS.md, D-010).

## What will live here

One adapter per retailer (for example `flipkart/`, `amazon/`, `croma/`,
`reliance/`, `vijaysales/`, `generic/`), each normalizing its output into a
common product/observation schema. Collector code stays isolated here so
no other part of the app depends on any one retailer's HTML structure
(D-004 in project-memory/DECISIONS.md).

## Before building the first collector

Read `project-memory/KNOWLEDGE/retailers.md` and `research.md` (open
question RQ-02): each retailer's terms of service and `robots.txt` need
reviewing, and no CAPTCHA bypassing or anti-bot circumvention is allowed
(D-008).
