import { useMemo } from "react";
import { useFetch } from "./useFetch";
import {
  getDealAssessment,
  getProductDetail,
  listOffers,
  listPriceObservations,
  listProducts,
  listRetailerListings,
  listRetailers,
} from "../lib/api";

export function useProducts() {
  return useFetch(() => listProducts(), []);
}

/** All retailers, fetched once -- used to look up a name from a
 * listing's retailer_id without denormalizing the backend response. */
export function useRetailers() {
  const { data, loading, error } = useFetch(() => listRetailers(), []);
  const byId = useMemo(() => new Map((data ?? []).map((retailer) => [retailer.id, retailer])), [data]);
  return { retailers: data ?? [], byId, loading, error };
}

export function useProductDetail(productId: number | null) {
  return useFetch(productId !== null ? () => getProductDetail(productId) : null, [productId]);
}

export function useListingsForVariant(productVariantId: number | null) {
  return useFetch(
    productVariantId !== null ? () => listRetailerListings({ productVariantId }) : null,
    [productVariantId],
  );
}

export function usePriceHistory(retailerListingId: number | null) {
  return useFetch(retailerListingId !== null ? () => listPriceObservations(retailerListingId) : null, [
    retailerListingId,
  ]);
}

export function useOffersForListing(retailerListingId: number | null) {
  return useFetch(retailerListingId !== null ? () => listOffers(retailerListingId) : null, [retailerListingId]);
}

export function useDealAssessment(retailerListingId: number | null) {
  return useFetch(retailerListingId !== null ? () => getDealAssessment(retailerListingId) : null, [
    retailerListingId,
  ]);
}
