import { Inbox } from "lucide-react";

/**
 * V0.1 has no retailer collectors, so there is no real deal data to show.
 * This deliberately does not display placeholder products or prices --
 * see project-memory/DECISIONS.md (D-005: never invent data).
 */
export function DealFeed() {
  return (
    <section className="flex min-h-[24rem] flex-col items-center justify-center rounded-lg border border-base-hairline bg-base-panel p-10 text-center">
      <Inbox className="mb-4 h-8 w-8 text-ink-muted" strokeWidth={1.5} aria-hidden="true" />
      <h2 className="mb-1.5 text-sm text-ink-muted">Deal feed</h2>
      <p className="max-w-sm text-sm text-ink-muted">
        No deals tracked yet. Retailer scanning isn't built in this version, so nothing here is discovered
        automatically. Add phones to your wishlist -- once collectors are connected in a later version, matching
        deals will start appearing here.
      </p>
    </section>
  );
}
