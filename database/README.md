# database/

Holds the local SQLite database file used by the backend in development:
`bbd_hunter.db`. It's created automatically the first time the backend
starts (`backend/app/database.py` calls `init_db()` on startup) -- there's
nothing to set up by hand.

`*.db` files in this folder are gitignored on purpose: the database is
local runtime data, not source code, and shouldn't be committed. This
README is tracked so the (otherwise empty) folder survives a git clone.

## Schema

Defined in code, not here -- see `backend/app/models/`. There is no
migration tool yet (a deliberate V0.1 scope cut). If a model's fields
change during development, the simplest fix is to delete `bbd_hunter.db`
and let it regenerate; introduce a real migration tool (e.g. Alembic)
before this matters for real data.
