import { useState } from "react";
import {
  useDealAssessment,
  useListingsForVariant,
  useOffersForListing,
  usePriceHistory,
  useProductDetail,
  useProducts,
  useRetailers,
} from "../../hooks/useExplorerData";
import { ProductListPanel } from "./ProductListPanel";
import { VariantListPanel } from "./VariantListPanel";
import { ListingsPanel } from "./ListingsPanel";
import { PriceHistoryList } from "./PriceHistoryList";
import { OffersList } from "./OffersList";
import { DealSignalsSummary } from "./DealSignalsSummary";

/**
 * A Products -> Variants -> Listings -> (History + Offers + Deal signals)
 * drill-down. Selecting something upstream clears anything selected
 * downstream of it, so the panels never show detail for a variant/listing
 * that no longer matches what's picked above it.
 */
export function DataExplorer() {
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);
  const [selectedVariantId, setSelectedVariantId] = useState<number | null>(null);
  const [selectedListingId, setSelectedListingId] = useState<number | null>(null);

  const products = useProducts();
  const retailers = useRetailers();
  const productDetail = useProductDetail(selectedProductId);
  const listings = useListingsForVariant(selectedVariantId);
  const priceHistory = usePriceHistory(selectedListingId);
  const offers = useOffersForListing(selectedListingId);
  const dealAssessment = useDealAssessment(selectedListingId);

  function handleSelectProduct(productId: number) {
    setSelectedProductId(productId);
    setSelectedVariantId(null);
    setSelectedListingId(null);
  }

  function handleSelectVariant(variantId: number) {
    setSelectedVariantId(variantId);
    setSelectedListingId(null);
  }

  return (
    <div className="mx-auto flex max-w-7xl flex-col gap-4 px-6 pb-10 pt-6">
      <div>
        <h1 className="text-lg font-semibold tracking-tight text-ink">Data Explorer</h1>
        <p className="text-sm text-ink-muted">
          Browse tracked products, retailer listings, price history, and offers. Items marked{" "}
          <span className="font-mono text-[11px] uppercase text-signal-amber">Demo</span> are fixture data for
          development, never real observed prices.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <ProductListPanel
          products={products.data ?? []}
          loading={products.loading}
          error={products.error}
          selectedProductId={selectedProductId}
          onSelect={handleSelectProduct}
        />
        <VariantListPanel
          product={productDetail.data}
          loading={productDetail.loading}
          error={productDetail.error}
          selectedVariantId={selectedVariantId}
          onSelect={handleSelectVariant}
        />
      </div>

      <ListingsPanel
        listings={listings.data}
        loading={listings.loading}
        error={listings.error}
        retailersById={retailers.byId}
        selectedListingId={selectedListingId}
        onSelect={setSelectedListingId}
      />

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <PriceHistoryList observations={priceHistory.data} loading={priceHistory.loading} error={priceHistory.error} />
        <OffersList offers={offers.data} loading={offers.loading} error={offers.error} />
        <DealSignalsSummary
          assessment={dealAssessment.data}
          loading={dealAssessment.loading}
          error={dealAssessment.error}
        />
      </div>
    </div>
  );
}
