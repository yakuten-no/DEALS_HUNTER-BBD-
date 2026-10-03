import type { DealAssessment } from "../../types/product";

interface DealSignalsSummaryProps {
  assessment: DealAssessment | null;
  loading: boolean;
  error: string | null;
}

/**
 * Shows the deal engine's own reasons/caveats verbatim rather than
 * re-deriving a "deal score" in the frontend -- the backend is the one
 * source of truth for these claims (D-005 in project-memory/DECISIONS.md).
 */
export function DealSignalsSummary({ assessment, loading, error }: DealSignalsSummaryProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <h2 className="mb-3 text-sm text-ink-muted">Deal signals</h2>

      {assessment === null && !loading && <p className="text-sm text-ink-muted">Select a listing to see its deal signals.</p>}
      {loading && <p className="text-sm text-ink-muted">Loading...</p>}
      {error && <p className="text-sm text-signal-negative">{error}</p>}

      {assessment && (
        <div className="flex flex-col gap-2">
          {assessment.reasons.map((reason) => (
            <p key={reason} className="text-sm text-signal-positive">
              {reason}
            </p>
          ))}
          {assessment.caveats.map((caveat) => (
            <p key={caveat} className="text-xs text-ink-muted">
              {caveat}
            </p>
          ))}
        </div>
      )}
    </section>
  );
}
