# ai/

Empty in V0.1. No AI is wired into the app yet -- the dashboard's system
status panel honestly shows "AI: Not connected" rather than faking it.

## What will live here

A provider abstraction (Ollama-compatible first, with room to add another
model later) used for interpretation, classification, summarization,
discovery, explanation, and review analysis -- never for deciding
financial actions on its own. Deterministic rules (maximum price, minimum
storage, required variant, availability, seller conditions) stay in the
backend's rule engine, not here. See D-003 in project-memory/DECISIONS.md
and the pipeline diagram in project-memory/ARCHITECTURE.md.
