import type { WishlistCreateInput, WishlistEntry, WishlistUpdateInput } from "../types/wishlist";
import type {
  DealAssessment,
  Offer,
  PriceObservation,
  ProductDetail,
  ProductListItem,
  Retailer,
  RetailerListingListItem,
} from "../types/product";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  database: "connected" | "error" | string;
}

function buildQuery(params: Record<string, string | number | boolean | undefined>): string {
  const entries = Object.entries(params).filter(([, value]) => value !== undefined) as [string, string | number | boolean][];
  if (entries.length === 0) return "";
  const search = new URLSearchParams(entries.map(([key, value]) => [key, String(value)]));
  return `?${search.toString()}`;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Request to ${path} failed (${response.status}): ${detail}`);
  }

  // DELETE returns 204 No Content -- there's no body to parse.
  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/api/health");
}

export function listWishlists(): Promise<WishlistEntry[]> {
  return request<WishlistEntry[]>("/api/wishlists");
}

export function createWishlist(data: WishlistCreateInput): Promise<WishlistEntry> {
  return request<WishlistEntry>("/api/wishlists", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function updateWishlist(id: number, data: WishlistUpdateInput): Promise<WishlistEntry> {
  return request<WishlistEntry>(`/api/wishlists/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export function deleteWishlist(id: number): Promise<void> {
  return request<void>(`/api/wishlists/${id}`, { method: "DELETE" });
}

// --- V0.2: product & deal data (read-only from the frontend for now --
// creating retailers/products/listings is done via the API directly or
// the seed script; the Data Explorer is a browsing experience) ---

export function listRetailers(): Promise<Retailer[]> {
  return request<Retailer[]>("/api/retailers");
}

export function listProducts(): Promise<ProductListItem[]> {
  return request<ProductListItem[]>("/api/products");
}

export function getProductDetail(productId: number): Promise<ProductDetail> {
  return request<ProductDetail>(`/api/products/${productId}`);
}

export function listRetailerListings(params: { productVariantId: number }): Promise<RetailerListingListItem[]> {
  return request<RetailerListingListItem[]>(
    `/api/retailer-listings${buildQuery({ product_variant_id: params.productVariantId })}`,
  );
}

export function listPriceObservations(retailerListingId: number): Promise<PriceObservation[]> {
  return request<PriceObservation[]>(
    `/api/price-observations${buildQuery({ retailer_listing_id: retailerListingId })}`,
  );
}

export function listOffers(retailerListingId: number): Promise<Offer[]> {
  return request<Offer[]>(`/api/offers${buildQuery({ retailer_listing_id: retailerListingId })}`);
}

export function getDealAssessment(retailerListingId: number, wishlistId?: number): Promise<DealAssessment> {
  return request<DealAssessment>(
    `/api/retailer-listings/${retailerListingId}/deal-assessment${buildQuery({ wishlist_id: wishlistId })}`,
  );
}
