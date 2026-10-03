import type { PriceObservation } from "../../types/product";

interface PriceHistoryListProps {
  observations: PriceObservation[] | null;
  loading: boolean;
  error: string | null;
}

function formatINR(value: number): string {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" });
}

export function PriceHistoryList({ observations, loading, error }: PriceHistoryListProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <h2 className="mb-3 text-sm text-ink-muted">Price history</h2>

      {observations === null && !loading && (
        <p className="text-sm text-ink-muted">Select a listing to see its price history.</p>
      )}
      {loading && <p className="text-sm text-ink-muted">Loading...</p>}
      {error && <p className="text-sm text-signal-negative">{error}</p>}
      {/* Only ever shows real, stored observations -- never a fabricated
          chart or placeholder price (see project-memory/DECISIONS.md, D-005). */}
      {observations && observations.length === 0 && (
        <p className="text-sm text-ink-muted">No price history available yet.</p>
      )}

      {observations && observations.length > 0 && (
        <>
          {observations[0].source_note && (
            <p className="mb-2 text-xs italic text-signal-amber">{observations[0].source_note}</p>
          )}
          <ul className="flex max-h-64 flex-col gap-1 overflow-y-auto">
            {observations.map((observation) => {
              const isLowest = observation.observed_price === Math.min(...observations.map((o) => o.observed_price));
              return (
                <li key={observation.id} className="flex items-center justify-between gap-3 text-sm">
                  <span className="text-ink-muted">{formatDate(observation.observed_at)}</span>
                  <span className={`font-mono ${isLowest ? "text-signal-positive" : "text-ink"}`}>
                    {formatINR(observation.observed_price)}
                    {observation.mrp != null && (
                      <span className="ml-1.5 text-ink-muted line-through">{formatINR(observation.mrp)}</span>
                    )}
                  </span>
                </li>
              );
            })}
          </ul>
        </>
      )}
    </section>
  );
}
