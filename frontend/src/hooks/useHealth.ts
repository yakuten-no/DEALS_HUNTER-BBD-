import { useEffect, useState } from "react";
import { getHealth, type HealthResponse } from "../lib/api";

export type BackendStatus = "checking" | "connected" | "offline";

const POLL_INTERVAL_MS = 15_000;

/**
 * Polls GET /api/health so the dashboard's system-status panel reflects
 * the backend's real, current state rather than a value fetched once and
 * left stale. There's no WebSocket push for this yet -- see
 * project-memory/ROADMAP.md -- so a plain interval is the V0.1 approach.
 */
export function useHealth() {
  const [status, setStatus] = useState<BackendStatus>("checking");
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function check() {
      try {
        const result = await getHealth();
        if (!cancelled) {
          setHealth(result);
          setStatus("connected");
        }
      } catch {
        if (!cancelled) {
          setHealth(null);
          setStatus("offline");
        }
      }
    }

    check();
    const interval = setInterval(check, POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  return { status, health };
}
