import { StatusDot, type StatusState } from "./StatusDot";
import type { BackendStatus } from "../../hooks/useHealth";
import type { HealthResponse } from "../../lib/api";

interface SystemStatusPanelProps {
  backendStatus: BackendStatus;
  health: HealthResponse | null;
}

/**
 * Backend and Database are live checks derived from GET /api/health.
 * AI and Collectors are honest static labels: V0.1 has neither, so they
 * always read "Not connected" / "Not running" -- never faked as active.
 */
export function SystemStatusPanel({ backendStatus, health }: SystemStatusPanelProps) {
  const backendState: StatusState =
    backendStatus === "connected" ? "connected" : backendStatus === "checking" ? "checking" : "offline";

  const databaseState: StatusState =
    health?.database === "connected" ? "connected" : backendStatus === "checking" ? "checking" : "offline";

  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <h2 className="mb-3 text-sm text-ink-muted">System</h2>
      <div className="flex flex-col gap-2.5">
        <StatusDot
          state={backendState}
          label="Backend"
          detail={backendState === "connected" ? "Connected" : backendState === "checking" ? "Checking..." : "Offline"}
        />
        <StatusDot
          state={databaseState}
          label="Database"
          detail={
            databaseState === "connected" ? "Connected" : databaseState === "checking" ? "Checking..." : "Not initialized"
          }
        />
        <StatusDot state="inactive" label="AI" detail="Not connected" />
        <StatusDot state="inactive" label="Collectors" detail="Not running" />
      </div>
    </section>
  );
}
