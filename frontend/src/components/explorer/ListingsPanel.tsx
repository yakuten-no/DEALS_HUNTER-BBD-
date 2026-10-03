import type { Retailer, RetailerListingListItem } from "../../types/product";
import { DemoBadge } from "./DemoBadge";

interface ListingsPanelProps {
  listings: RetailerListingListItem[] | null;
  loading: boolean;
  error: string | null;
  retailersById: Map<number, Retailer>;
  selectedListingId: number | null;
  onSelect: (listingId: number) => void;
}

function formatINR(value: number): string {
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value);
}

const AVAILABILITY_LABEL: Record<string, string> = {
  in_stock: "In stock",
  out_of_stock: "Out of stock",
  unknown: "Availability unknown",
};

export function ListingsPanel({
  listings,
  loading,
  error,
  retailersById,
  selectedListingId,
  onSelect,
}: ListingsPanelProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <h2 className="mb-3 text-sm text-ink-muted">Listings</h2>

      {listings === null && !loading && <p className="text-sm text-ink-muted">Select a variant to see its listings.</p>}
      {loading && <p className="text-sm text-ink-muted">Loading...</p>}
      {error && <p className="text-sm text-signal-negative">{error}</p>}
      {listings && !loading && listings.length === 0 && (
        <p className="text-sm text-ink-muted">No retailer listings tracked for this variant yet.</p>
      )}

      {listings && listings.length > 0 && (
        <ul className="flex flex-col gap-1.5">
          {listings.map((listing) => {
            const isSelected = listing.id === selectedListingId;
            const retailerName = retailersById.get(listing.retailer_id)?.name ?? `Retailer #${listing.retailer_id}`;
            return (
              <li key={listing.id}>
                <button
                  type="button"
                  onClick={() => onSelect(listing.id)}
                  className={`flex w-full items-center justify-between gap-3 rounded-md border px-3 py-2 text-left transition-colors ${
                    isSelected
                      ? "border-signal-amber/60 bg-signal-amber/10"
                      : "border-base-hairline bg-base hover:border-signal-amber/30"
                  }`}
                >
                  <span className="min-w-0 flex-1">
                    <span className="flex items-center gap-1.5">
                      <span className="truncate text-sm text-ink">{retailerName}</span>
                      {listing.is_demo && <DemoBadge />}
                    </span>
                    <span className="block truncate text-xs text-ink-muted">
                      {listing.listing_title ?? listing.product_url}
                    </span>
                  </span>
                  <span className="flex flex-shrink-0 flex-col items-end gap-0.5">
                    <span className="font-mono text-sm text-ink">
                      {listing.latest_price != null ? formatINR(listing.latest_price) : "No price yet"}
                    </span>
                    <span
                      className={`text-[11px] ${
                        listing.availability === "in_stock"
                          ? "text-signal-positive"
                          : listing.availability === "out_of_stock"
                            ? "text-signal-negative"
                            : "text-ink-muted"
                      }`}
                    >
                      {AVAILABILITY_LABEL[listing.availability] ?? listing.availability}
                    </span>
                  </span>
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </section>
  );
}
