/**
 * Mirrors backend/app/models/{retailer,product,product_variant,retailer_listing,
 * price_observation,offer}.py and backend/app/deal_engine/assessment.py.
 * V0.2 has no shared-schema code generation, same as wishlist.ts -- keep
 * these in sync by hand when either side changes.
 */

export interface Retailer {
  id: number;
  name: string;
  slug: string;
  website: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Product {
  id: number;
  brand: string;
  model_name: string;
  normalized_name: string;
  category: string;
  description: string | null;
  is_demo: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductListItem extends Product {
  variant_count: number;
}

export interface ProductVariant {
  id: number;
  product_id: number;
  storage_gb: number | null;
  ram_gb: number | null;
  color: string | null;
  variant_name: string | null;
  sku: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProductDetail extends Product {
  variants: ProductVariant[];
}

export type AvailabilityStatus = "in_stock" | "out_of_stock" | "unknown";

export interface RetailerListing {
  id: number;
  retailer_id: number;
  product_variant_id: number;
  seller_name: string | null;
  external_listing_id: string | null;
  product_url: string;
  listing_title: string | null;
  availability: AvailabilityStatus;
  is_demo: boolean;
  created_at: string;
  updated_at: string;
}

export interface RetailerListingListItem extends RetailerListing {
  latest_price: number | null;
  latest_observed_at: string | null;
}

export interface PriceObservation {
  id: number;
  retailer_listing_id: number;
  observed_price: number;
  mrp: number | null;
  currency: string;
  source_note: string | null;
  observed_at: string;
  created_at: string;
}

export type OfferType =
  | "bank_discount"
  | "coupon"
  | "exchange_bonus"
  | "cashback"
  | "emi_offer"
  | "card_discount"
  | "instant_discount"
  | "other";

export interface Offer {
  id: number;
  retailer_listing_id: number;
  offer_type: OfferType;
  title: string;
  description: string | null;
  discount_amount: number | null;
  discount_percentage: number | null;
  is_guaranteed: boolean;
  conditions: string | null;
  valid_from: string | null;
  valid_until: string | null;
  created_at: string;
  updated_at: string;
}

export interface DealSignals {
  has_price_history: boolean;
  observation_count: number;
  price_dropped_from_previous_observation: boolean | null;
  lowest_observed_in_history: boolean | null;
  within_wishlist_target: boolean | null;
  within_wishlist_max: boolean | null;
  has_guaranteed_discount: boolean;
  has_conditional_offers: boolean;
  has_cashback_offers: boolean;
  is_available: boolean | null;
}

export interface DealAssessment {
  retailer_listing_id: number;
  assessed_at: string;
  listing_availability: string;
  current_price: number | null;
  mrp: number | null;
  mrp_discount_percentage: number | null;
  lowest_observed_price: number | null;
  highest_observed_price: number | null;
  average_observed_price: number | null;
  guaranteed_discount_total: number;
  conditional_discount_total: number;
  cashback_total: number;
  effective_price_guaranteed: number | null;
  potential_effective_price: number | null;
  signals: DealSignals;
  reasons: string[];
  caveats: string[];
}
