import type { ActivityEntry } from "../../hooks/useActivityLog";

interface ActivityLogProps {
  entries: ActivityEntry[];
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
}

export function ActivityLog({ entries }: ActivityLogProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <h2 className="mb-3 text-sm text-ink-muted">Activity</h2>
      {entries.length === 0 ? (
        <p className="text-sm text-ink-muted">Nothing yet this session.</p>
      ) : (
        <ul className="flex max-h-64 flex-col gap-2 overflow-y-auto">
          {entries.map((entry) => (
            <li key={entry.id} className="animate-insert-row flex items-baseline gap-2 text-sm">
              <span className="flex-shrink-0 font-mono text-xs text-ink-muted">{formatTime(entry.timestamp)}</span>
              <span className="text-ink/90">{entry.message}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
