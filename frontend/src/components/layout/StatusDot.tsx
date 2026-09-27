export type StatusState = "connected" | "offline" | "checking" | "inactive";

interface StatusDotProps {
  state: StatusState;
  label: string;
  detail?: string;
}

const STATE_STYLES: Record<StatusState, { dot: string; text: string; pulse?: boolean }> = {
  connected: { dot: "bg-signal-positive", text: "text-ink", pulse: true },
  offline: { dot: "bg-signal-negative", text: "text-ink/70" },
  checking: { dot: "bg-signal-amber", text: "text-ink/70", pulse: true },
  inactive: { dot: "bg-ink-muted/40", text: "text-ink-muted" },
};

export function StatusDot({ state, label, detail }: StatusDotProps) {
  const styles = STATE_STYLES[state];
  return (
    <div className="flex items-center gap-2">
      <span
        className={`h-2 w-2 flex-shrink-0 rounded-full ${styles.dot} ${styles.pulse ? "animate-pulse-dot" : ""}`}
        aria-hidden="true"
      />
      <span className={`text-sm ${styles.text}`}>{label}</span>
      {detail && <span className="ml-auto font-mono text-xs text-ink-muted">{detail}</span>}
    </div>
  );
}
