import type { Offer } from "../../types/product";

interface OffersListProps {
  offers: Offer[] | null;
  loading: boolean;
  error: string | null;
}

function formatDiscount(offer: Offer): string | null {
  if (offer.discount_amount != null) return `\u20b9${offer.discount_amount.toLocaleString("en-IN")} off`;
  if (offer.discount_percentage != null) return `${offer.discount_percentage}% off`;
  return null;
}

export function OffersList({ offers, loading, error }: OffersListProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <h2 className="mb-3 text-sm text-ink-muted">Offers</h2>

      {offers === null && !loading && <p className="text-sm text-ink-muted">Select a listing to see its offers.</p>}
      {loading && <p className="text-sm text-ink-muted">Loading...</p>}
      {error && <p className="text-sm text-signal-negative">{error}</p>}
      {offers && offers.length === 0 && <p className="text-sm text-ink-muted">No offers available.</p>}

      {offers && offers.length > 0 && (
        <ul className="flex flex-col gap-2">
          {offers.map((offer) => (
            <li key={offer.id} className="rounded-md border border-base-hairline bg-base p-2.5">
              <div className="flex items-start justify-between gap-2">
                <span className="text-sm text-ink">{offer.title}</span>
                <span
                  className={`flex-shrink-0 rounded px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wide ${
                    offer.is_guaranteed
                      ? "border border-signal-positive/40 text-signal-positive"
                      : "border border-ink-muted/40 text-ink-muted"
                  }`}
                >
                  {offer.is_guaranteed ? "Guaranteed" : "Conditional"}
                </span>
              </div>
              {formatDiscount(offer) && <p className="mt-1 font-mono text-xs text-ink-muted">{formatDiscount(offer)}</p>}
              {offer.conditions && <p className="mt-1 text-xs text-ink-muted">{offer.conditions}</p>}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
