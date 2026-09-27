import { Radar } from "lucide-react";

export function Header() {
  return (
    <header className="border-b border-base-hairline">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
        <div className="flex items-center gap-2.5">
          <Radar className="h-5 w-5 text-signal-amber" strokeWidth={1.75} aria-hidden="true" />
          <span className="text-lg font-semibold tracking-tight text-ink">BBD Hunter</span>
        </div>
        <p className="hidden text-sm text-ink-muted sm:block">Shopping intelligence for smartphones in India</p>
      </div>
    </header>
  );
}
