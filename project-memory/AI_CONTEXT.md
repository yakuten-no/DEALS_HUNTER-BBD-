# BBD HUNTER — AI Context (read this first)

> Primary handoff file for any AI agent. Keep it short (aim for ~120 lines or fewer); put detail in the other `project-memory/` files.
> Last updated: 2026-09-21 (session date; container UTC clock read 2026-09-20T22:25Z) · Memory layer version: V0.1

**STATE CONFIDENCE: LOW.** This memory layer was created in a session that had **no access to the BBD HUNTER repository** (no repo, uploads, or earlier transcripts were present). Everything below about code is `[UNVERIFIED]`. If you can see the repository, inspect it first and reconcile these files (TODO T-001; `MEMORY_PROTOCOL.md` rule 14). Do not trust this file over the code.

Status tags: `[VERIFIED]` confirmed by inspecting or running the repo · `[PLANNED]` intended, not built · `[UNVERIFIED]` believed, not checked · `[UNKNOWN]` no information.

## 1. What BBD HUNTER is
A local-first AI shopping-intelligence and deal-hunting app, initially for **smartphones in India**. Goal: answer "what is the best deal available for MY requirements right now?", not just "did a price drop?". It turns natural-language needs into structured preferences, tracks prices across Indian retailers, keeps price history, detects genuine drops and record lows, separates guaranteed from conditional discounts, and has a fast **Hunt Mode** for sale events (for example Flipkart Big Billion Days). Browser-assisted checkout is a distant goal and always human-controlled. Details: `PROJECT.md`.

## 2. Current version
- Target: **V0.1 (foundation)**.
- Actual code version: `[UNKNOWN]`.
- Memory layer: V0.1, created 2026-09-21.

## 3. Current objective
1. Done: create the portable project memory in `project-memory/`.
2. Next: inspect the real repository and reconcile memory with it (T-001).
3. Then: finish the V0.1 foundation (scope in section 6). No scraping and no checkout automation in V0.1.

## 4. Completed work
- `[VERIFIED]` User-authored Master Project Instructions exist (goals, philosophy, stack, V0.1 scope). Whether a copy is stored in the repo is `[UNKNOWN]`.
- `[VERIFIED]` `project-memory/` created with 14 files on 2026-09-21.
- No application code is confirmed. None was found in the memory-creation environment.

## 5. Work in progress
- V0.1 foundation scaffold: `[UNKNOWN]` whether any of it exists.

## 6. Next tasks (full list: `TODO.md`)
1. T-001 Reconcile memory with the real repository; record the actual V0.1 status in `CURRENT_STATE.md`.
2. V0.1 scope: repository structure · frontend shell · backend shell · database shell · configuration system (`.env.example`) · premium dashboard UI · health/status endpoint · basic wishlist model · development docs.
3. Later phases: `ROADMAP.md` (only V0.1 is user-defined; later phases are proposals awaiting approval).

## 7. Important architectural decisions (full text: `DECISIONS.md`)
- D-001 Local-first: must run on a Windows PC; no required paid cloud backend or paid AI API.
- D-003 AI interprets and explains; a **deterministic rule engine decides**. An LLM never triggers financial actions on free-form reasoning.
- D-004 One isolated collector adapter per retailer, all normalizing to a common schema.
- D-005 Never invent data; mark uncertainty; say "lowest observed in our history" unless history supports "all-time low".
- D-006 Keep base price, guaranteed discount, conditional discount and cashback separate; show "Potential effective price" for uncertain ones.
- D-007 Never compare non-equivalent variants (RAM, storage, condition, region) as identical.
- D-008 Checkout security steps stay human-controlled; no CAPTCHA bypass or anti-bot circumvention; no secrets stored.
- D-011 Project memory is vendor-independent Markdown; no vector DB or SaaS memory for now.

## 8. Known bugs and blockers
- Bugs: none recorded. Code was not inspected, so this means `[UNKNOWN]`, not "bug-free". See `BUGS.md`.
- Blocker: the repository was not accessible when memory was created, so code state is unverified.
- Open architectural questions: `ARCHITECTURE.md` section 11.

## 9. Important files and directories
- `project-memory/` — this memory layer. Read `AI_CONTEXT.md` (this file) first, then `CURRENT_STATE.md`.
- Intended layout from the Master Instructions (`[UNVERIFIED]` that any of it exists; may change after architectural review): `frontend/`, `backend/`, `collectors/`, `ai/`, `deal_engine/`, `database/`, `automation/`, `notifications/`, `tests/`, `docs/`.
- Planned: `.env.example` for configuration (no secrets committed).

## 10. Technology stack (preferred initial stack, D-002)
- Frontend: React, Vite, TypeScript, Tailwind CSS, Framer Motion, Lucide icons.
- Backend: Python, FastAPI, asyncio.
- Database: SQLite.
- Browser automation: Playwright.
- Realtime: WebSockets.
- AI: Ollama-compatible local models behind a provider abstraction.
- Runtime target: a Windows PC, run locally.

## 11. Constraints
- Never invent prices, discounts, specs, availability or offers. Mark uncertain information as uncertain.
- Never request or store passwords, UPI PINs, card CVVs, OTPs or authentication secrets. No CAPTCHA bypass. No anti-bot circumvention.
- No dependency on a paid AI API. Avoid unnecessary cloud dependencies.
- Build incrementally: explain the architecture briefly, build the smallest working version, test, fix, continue. Preserve working functionality. Do not rewrite working architecture for style.
- The user is a beginner/intermediate developer: explain decisions in plain language, give complete files (labelled `FILE: path/to/file`), give exact install commands, and never assume a dependency is installed.
- Code: TypeScript types, Python type hints, configuration via environment variables, tests for major components.
- Memory: no secrets, no large code copies, follow `MEMORY_PROTOCOL.md`.

## 12. Last updated
2026-09-21 (session date) · container UTC clock read 2026-09-20T22:25Z · written by an AI agent (vendor-neutral record).
