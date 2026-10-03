# BBD HUNTER — Project Overview

> Purpose: what BBD HUNTER is, who it is for, what it should do, and where it is heading.
> Last updated: 2026-09-21 · Memory layer V0.1
> Source: distilled from the user's Master Project Instructions. Nothing here claims implemented code (see `CURRENT_STATE.md`).

## What it is
BBD HUNTER is a **local-first AI shopping-intelligence and deal-hunting application**, focused initially on **smartphones in India**. It is not merely a price tracker. The question it exists to answer is:

> "What is the best deal available for MY requirements right now?"

rather than "Did this product become cheaper?"

Name: "BBD" presumably refers to Flipkart's Big Billion Days sale. `[UNVERIFIED]` — inferred from the Master Instructions, not stated there.

## Purpose
Help a shopper find genuinely good smartphone deals, especially during big sale events, by combining personal requirements, tracked price history, transparent offer calculations, and product/spec/review intelligence, while staying honest about what is known and what is uncertain.

## Target users
- Primary: the project owner, a beginner-to-intermediate developer building and running the app locally on a Windows PC.
- Wider audience beyond the owner: `[UNKNOWN]` (not specified).

## Product philosophy
- Facts first: never invent prices, discounts, specifications, availability or offers. Mark uncertainty explicitly.
- An advertised MRP discount is not proof of a genuine deal. Genuine deals are judged against stored price history.
- Transparent calculations: guaranteed discounts, conditional discounts and cashback are kept separate.
- AI interprets and explains; deterministic rules decide anything with financial consequences.
- Local-first: no required paid cloud backend, no required paid AI API.
- The human stays in control of security-sensitive steps (CAPTCHA, OTP, payment authorization).

## Major capabilities (all `[PLANNED]` unless `CURRENT_STATE.md` says otherwise)
1. Understand shopping requirements in natural language and convert them to structured preferences.
2. Discover relevant smartphones across Indian retailers.
3. Track prices and keep historical observations.
4. Detect genuine price drops and record-low prices.
5. Identify discounts and offers; distinguish guaranteed from conditional discounts.
6. Compare equivalent phone variants correctly (model, RAM, storage, condition, region, seller).
7. Analyze phone specifications and normalize them across manufacturers.
8. Analyze reviews and recurring complaints; flag suspicious or inconsistent listings.
9. Discover deals the user did not explicitly add to the wishlist.
10. Notify the user when configured conditions are met.
11. Provide a fast Hunt Mode for major sale events.
12. Eventually support browser-assisted checkout, with CAPTCHA, OTP, payment authorization and similar confirmations left to the human.

## Operating modes
- **Normal Mode**: personalized deal feed, wishlist, price history, deal discoveries, price/offer/stock changes, recently discovered products, AI explanations.
- **Hunt Mode**: for sale events. Prioritizes speed, exact wishlist targets, price and stock changes, variant availability, deal triggers and immediate notifications. Minimizes UI activity and surfaces only actionable events.

## How AI and rules divide the work
User → AI interpretation → structured preferences → deterministic rule engine → deal engine → automation.
- AI: interpretation, classification, summarization, discovery, explanation, review analysis.
- Deterministic rules: maximum price, minimum storage, required variant, required availability, required seller conditions, explicit user constraints.

## Experience goals
Fast, premium, modern, minimal, information-dense without clutter. A clean, futuristic interface rather than a generic admin dashboard; subtle animation; excellent typography. Inspired by Nothing OS's visual simplicity without copying Nothing's proprietary design. Excellent on desktop, responsive on smaller screens, and extremely clear during sale events.

## Technology direction (summary; see `ARCHITECTURE.md`)
React + Vite + TypeScript + Tailwind + Framer Motion + Lucide (frontend); Python + FastAPI + asyncio (backend); SQLite; Playwright; WebSockets; Ollama-compatible local AI behind a provider abstraction. Runs locally on Windows.

## Long-term vision
An AI shopping-intelligence system that knows the user's requirements, watches the market continuously, tells the user when a deal is genuinely good and why, and can eventually assist checkout in the browser with the human confirming every security-sensitive step. Expansion beyond smartphones or India is implied by "initially" but is `[UNKNOWN]` and unplanned.

## Where to look next
- Fast handoff: `AI_CONTEXT.md` · Current status: `CURRENT_STATE.md`
- What is wanted: `REQUIREMENTS.md` · How it is built: `ARCHITECTURE.md`
- Why choices were made: `DECISIONS.md` · What comes next: `ROADMAP.md`, `TODO.md`
