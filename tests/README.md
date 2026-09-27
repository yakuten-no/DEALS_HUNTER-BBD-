# tests/

This top-level folder is intentionally close to empty right now. Tests for
V0.1 live next to the code they test, not here:

- Backend tests: `backend/tests/` (pytest) -- needs to sit inside
  `backend/` so `app` is importable without installing the project as a
  package (see `backend/pytest.ini`).
- Frontend tests: colocated with their source files under `frontend/src/`
  (e.g. `App.test.tsx` next to `App.tsx`), the standard Vitest convention.

This folder is reserved for future cross-cutting tests that span more than
one system -- for example an end-to-end test that drives the real frontend
against the real backend, once there's more than one system to integrate.
That doesn't exist yet in V0.1.
