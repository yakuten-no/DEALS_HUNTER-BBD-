# BBD Hunter

A local-first AI shopping intelligence and deal-hunting app, focused
initially on smartphones in India. The goal is to answer *"what's the best
deal available for my requirements right now?"* -- not just *"did this
product get cheaper?"* Full product vision: `project-memory/PROJECT.md`.

> **Status:** V0.1 (foundation) is confirmed built and running. This
> update adds **V0.2: Product & Deal Data Foundation** -- the normalized
> data model, deal engine, and Data Explorer described below. V0.2 was
> built the same way V0.1 was, in a sandboxed environment with no
> internet access, so **it has not been run end-to-end here either** --
> see [A note on how this was verified](#a-note-on-how-this-was-verified).
> Re-running Setup below (`pip install` / `npm install` again picks up
> the new backend dependencies -- there are none new, but re-running is
> harmless) is the first real test of V0.2's code.

## What's in V0.2

V0.2 adds the normalized data architecture that future retailer
collectors, price tracking, and AI will build on. **No live retailer
scraping, no AI, still no checkout automation** -- this is the engine and
data model, not live collection (see `project-memory/ROADMAP.md`).

What V0.2 adds on top of V0.1:
- **Product & deal data model**: Retailer, Product, ProductVariant,
  RetailerListing, PriceObservation (append-only -- history is never
  overwritten), and Offer, with real foreign keys and uniqueness
  constraints so, e.g., an 8GB/128GB phone and a 12GB/256GB phone can
  never collapse into one row.
- **A deterministic deal engine** (`backend/app/deal_engine/`): given a
  listing's price history and offers, computes transparent signals
  (price dropped? lowest we've seen? within your wishlist budget?
  guaranteed vs. conditional discount, cashback tracked separately) --
  never a single opaque "deal score", and never invents history that
  isn't there.
- **Deterministic product-name normalization** (`backend/app/normalization.py`):
  parses a retailer-style title like "Nothing Phone 3a Pro 12GB 256GB
  Black" into brand/RAM/storage/color -- pattern matching, no AI.
  no AI, no fuzzy matching.
- **A Data Explorer** in the frontend: browse Products -> Variants ->
  Retailer Listings -> Price History / Offers / Deal Signals. Shows only
  real stored data -- "No price history available yet." / "No offers
  available." where there's nothing to show, never a fabricated chart.
- **Optional, clearly-labelled demo/fixture data** (`backend/scripts/seed_demo_data.py`)
  for exercising the Explorer during development -- never run
  automatically, never mistaken for real pricing (see its own docstring).
- 81 new backend tests (99 total) and 6 new frontend tests (14 total).

## What's in V0.1 (unchanged, still the base this builds on)

V0.1 is the foundation: a FastAPI backend with a real health/status
check and full wishlist CRUD; a wishlist domain model with the fields a
future rule engine and AI layer will need; a React dashboard (hunt input,
wishlist, live system status, honest empty deal feed, activity log); and
tests for both. Full V0.1 detail is unchanged from before -- see the API
reference and project structure below, which now include V0.2's
additions alongside it.

## Project structure

```
BBD/
├── README.md                 <- you are here
├── .gitignore
├── project-memory/           <- project context for humans and AI agents; start at AI_CONTEXT.md
├── backend/                  <- FastAPI + SQLModel + SQLite
│   └── app/
│       ├── main.py           <- entry point, CORS, shared V0.2 error handlers
│       ├── config.py         <- settings from environment variables
│       ├── database.py       <- SQLite engine + session + foreign-key enforcement
│       ├── normalization.py  <- deterministic product-name parsing (V0.2)
│       ├── deal_engine/      <- deterministic deal assessment (V0.2)
│       ├── models/           <- SQLModel tables + API schemas (wishlist + V0.2 product/deal entities)
│       ├── routers/          <- API endpoints
│       └── services/         <- business logic (kept separate from routes)
│   └── scripts/
│       └── seed_demo_data.py <- optional, clearly-labelled demo data (V0.2)
├── frontend/                 <- React + TypeScript + Vite + Tailwind
│   └── src/
│       ├── App.tsx            <- dashboard layout + Dashboard/Data Explorer tab switch
│       ├── components/        <- layout, hunt input, wishlist, deal feed, activity, explorer (V0.2)
│       ├── hooks/              <- data fetching and local state
│       ├── lib/api.ts          <- typed backend client
│       └── types/               <- TypeScript types mirroring the backend schemas
├── collectors/                <- empty; future retailer adapters (see its README -- now describes the V0.2 schema to target)
├── ai/                         <- empty; future AI provider layer (see its README)
├── automation/                 <- empty; future background workers (see its README)
├── database/                   <- local SQLite file lives here at runtime (see its README)
└── tests/                       <- see its README for why tests actually live elsewhere
```

## Prerequisites

- **Python 3.11 or newer** (3.12 recommended). Check with `python3 --version` (macOS/Linux) or `python --version` (Windows).
- **Node.js 20 or newer**, which includes npm. Check with `node --version`.

If you don't have these yet, install Python from [python.org](https://www.python.org/downloads/) and Node.js from [nodejs.org](https://nodejs.org/) (the LTS version).

## Setup

Do these two sections in separate terminal windows -- the backend and frontend run as two separate processes during development.

### 1. Backend

**Windows (PowerShell):**
```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

**macOS / Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

You should see Uvicorn log that it's running on `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/api/health` in a browser -- you should get back JSON like:
```json
{"status": "ok", "service": "bbd-hunter", "version": "0.1.0", "database": "connected"}
```
The first request also creates `database/bbd_hunter.db` automatically -- there's no separate setup step for the database.

Interactive API docs (auto-generated by FastAPI) are at `http://127.0.0.1:8000/docs`.

### 2. Frontend

**Windows (PowerShell) or macOS / Linux -- same commands:**
```bash
cd frontend
npm install
copy .env.example .env    # Windows
cp .env.example .env      # macOS / Linux
npm run dev
```

Open the URL Vite prints (typically `http://localhost:5173`). The dashboard should load and its system status panel should show Backend and Database as **Connected** within a few seconds, as long as the backend from step 1 is still running.

### Something not connecting?

- **Frontend can't reach the backend / status shows Offline:** confirm the backend terminal is still running and shows no errors; confirm `frontend/.env`'s `VITE_API_BASE_URL` matches the URL Uvicorn printed (default `http://localhost:8000`); check the browser console for a CORS error, in which case confirm `backend/.env`'s `CORS_ORIGINS` includes the exact URL Vite printed.
- **`pip install` or `npm install` fails:** re-run it -- these need real internet access, which this project was built without (see the note at the bottom of this file). Confirm you're online.
- **Port already in use:** `uvicorn app.main:app --reload --port 8001` (and update `VITE_API_BASE_URL` to match), or `npm run dev -- --port 5174`.

## Running the tests

### Backend
```bash
cd backend
# with venv activated, from the Setup step above
pytest
```
Runs 115 tests: V0.1's original 18 (health + wishlist CRUD), 81 V0.2 tests
covering retailers, products, product variants, retailer
listings, price observations (including that history is genuinely never
overwritten), offers, product-name normalization, and all six deal-engine
scenarios named in the V0.2 brief (under budget, over budget, price drop,
no history, a conditional offer, an unavailable listing), and 16 regression
tests for the timezone-aware-UTC datetime convention and the clean 409 on
duplicate values. Tests run
against an isolated in-memory database -- they never touch your real
`database/bbd_hunter.db`.

### Frontend
```bash
cd frontend
npm test
```
Runs 14 tests: V0.1's original 8 plus 6 new ones for the Data Explorer
(product listing, empty states, the Products -> Variants drill-down, and
demo-data badging) and the new Dashboard/Data Explorer tab switch.

## Seeing it with data: optional demo seed

V0.2 ships no live collectors, so a fresh database has nothing to browse
in the Data Explorer. To see it populated during development:
```bash
cd backend
# with venv activated
python -m scripts.seed_demo_data
```
This creates a **fictional** "Democorp Demo Phone" product, across a
couple of variants and (real-name, reference-only) retailers, with a
price history and some offers -- every row it creates has `is_demo=true`
and is clearly labelled, and the frontend badges it visibly. It's never
run automatically (not on backend startup, not in tests) and is safe to
run more than once. See the script's own docstring for exactly what it
creates and why that's not a shortcut around "never invent real prices."

## API reference

### V0.1
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Backend + database status |
| POST | `/api/wishlists` | Create a wishlist entry |
| GET | `/api/wishlists` | List all wishlist entries |
| GET | `/api/wishlists/{id}` | Get one entry |
| PUT | `/api/wishlists/{id}` | Update an entry (only the fields you send are changed) |
| DELETE | `/api/wishlists/{id}` | Delete an entry |

### V0.2
| Method | Path | Purpose |
|---|---|---|
| POST, GET | `/api/retailers`, `/api/retailers/{id}` | Retailer reference data (no DELETE -- deactivate with `is_active`) |
| PUT | `/api/retailers/{id}` | Update (partial) |
| POST, GET | `/api/products`, `/api/products/{id}` | Products (detail view nests variants) |
| PUT, DELETE | `/api/products/{id}` | Update / delete (blocked with 409 if it still has variants) |
| POST, GET | `/api/product-variants`, `/api/product-variants/{id}` | Variants; `GET` supports `?product_id=` |
| PUT, DELETE | `/api/product-variants/{id}` | Update / delete (blocked with 409 if it still has listings) |
| POST, GET | `/api/retailer-listings`, `/api/retailer-listings/{id}` | Listings; `GET` supports `?product_variant_id=`, `?retailer_id=`, `?is_demo=` |
| PUT, DELETE | `/api/retailer-listings/{id}` | Update / delete (blocked with 409 if it still has price history or offers) |
| GET | `/api/retailer-listings/{id}/deal-assessment` | Deterministic deal signals; optional `?wishlist_id=` to compare against a budget |
| POST, GET | `/api/price-observations` | Create + list only (`?retailer_listing_id=` required for list) -- no update/delete, history is append-only |
| POST, GET | `/api/offers`, `/api/offers/{id}` | Offers; `GET` supports `?retailer_listing_id=` |
| PUT, DELETE | `/api/offers/{id}` | Update / delete |

Full request/response schemas: `http://127.0.0.1:8000/docs` while the backend is running.

## Project memory

This project keeps its own context in plain Markdown under `project-memory/`, independent of any specific AI tool. If you're an AI agent picking up this project, **read `project-memory/AI_CONTEXT.md` first**, then `project-memory/MEMORY_PROTOCOL.md` for the rules to follow while working on it.

## A note on how this was verified

V0.1 and the first V0.2 build were written in a sandbox with no internet, so
neither had ever been run. V0.2 was then taken over and run for real
(2026-10-01), which found and fixed four defects -- see `project-memory/BUGS.md`:
every database write failed on current SQLModel because timestamps were naive
(all timestamps are now timezone-aware UTC); every frontend test suite failed
on the Vitest setup; duplicate unique values crashed instead of returning 409;
and one test helper reused unique values.

**Actually executed** (Linux sandbox, Python 3.12, Node 22, SQLModel 0.0.47):
- Backend `pytest`: **115 passed, 0 failed.**
- Frontend `npm test`: **14 passed, 0 failed.**
- Frontend `npm run build` (includes the strict TypeScript check): **succeeded.**
- A real `uvicorn` server with the seed script on a throwaway database: health,
  wishlist CRUD, listings, price history, deal assessment (with and without
  history) and the 409 on duplicates all behaved correctly, with no server errors.
- The frontend's TypeScript types were compared against the backend's OpenAPI
  schemas: they match field for field.

**Not yet done:**
- Running everything on a Windows PC (please run the Setup and test commands
  above; `requirements.txt` now needs `sqlmodel>=0.0.47`).
- Clicking through the Data Explorer in a real browser -- the UI is covered by
  automated tests and a clean build only.

**Known open issue:** the deal assessment does not yet ignore offers whose
validity window has passed (BUG-006), so an expired offer is still counted.
