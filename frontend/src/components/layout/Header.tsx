import { Radar } from "lucide-react";

export type DashboardView = "dashboard" | "explorer";

interface HeaderProps {
  activeView: DashboardView;
  onViewChange: (view: DashboardView) => void;
}

const TABS: { id: DashboardView; label: string }[] = [
  { id: "dashboard", label: "Dashboard" },
  { id: "explorer", label: "Data Explorer" },
];

export function Header({ activeView, onViewChange }: HeaderProps) {
  return (
    <header className="border-b border-base-hairline">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-6 py-5">
        <div className="flex items-center gap-2.5">
          <Radar className="h-5 w-5 text-signal-amber" strokeWidth={1.75} aria-hidden="true" />
          <span className="text-lg font-semibold tracking-tight text-ink">BBD Hunter</span>
        </div>

        <nav className="flex items-center gap-1 rounded-md border border-base-hairline bg-base-panel p-1">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => onViewChange(tab.id)}
              aria-pressed={activeView === tab.id}
              className={`rounded px-3 py-1.5 text-sm transition-colors ${
                activeView === tab.id ? "bg-signal-amber text-base" : "text-ink-muted hover:text-ink"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        <p className="hidden text-sm text-ink-muted xl:block">Shopping intelligence for smartphones in India</p>
      </div>
    </header>
  );
}
