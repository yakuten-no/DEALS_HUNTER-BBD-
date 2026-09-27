import { useCallback, useState } from "react";

export interface ActivityEntry {
  id: string;
  message: string;
  timestamp: string;
}

const MAX_ENTRIES = 50;

/**
 * A session-only log of things that happened in this dashboard session
 * (backend connected, wishlist created, ...). It lives in React state and
 * is not persisted -- it resets on page reload. A real event history,
 * backed by the database, is future work (see project-memory/TODO.md);
 * this is deliberately not pretending to be that yet.
 */
export function useActivityLog() {
  const [entries, setEntries] = useState<ActivityEntry[]>([]);

  const log = useCallback((message: string) => {
    const entry: ActivityEntry = {
      id: crypto.randomUUID(),
      message,
      timestamp: new Date().toISOString(),
    };
    setEntries((prev) => [entry, ...prev].slice(0, MAX_ENTRIES));
  }, []);

  return { entries, log };
}
