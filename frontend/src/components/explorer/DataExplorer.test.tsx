import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { DataExplorer } from "./DataExplorer";
import * as api from "../../lib/api";
import type { ProductDetail, ProductListItem, Retailer, RetailerListingListItem } from "../../types/product";

vi.mock("../../lib/api");

const PRODUCT: ProductListItem = {
  id: 1,
  brand: "Nothing",
  model_name: "Phone 3a",
  normalized_name: "nothing phone 3a",
  category: "smartphone",
  description: null,
  is_demo: false,
  created_at: "2026-01-01T00:00:00",
  updated_at: "2026-01-01T00:00:00",
  variant_count: 1,
};

const PRODUCT_DETAIL: ProductDetail = {
  ...PRODUCT,
  variants: [
    {
      id: 10,
      product_id: 1,
      storage_gb: 128,
      ram_gb: 8,
      color: "Black",
      variant_name: null,
      sku: null,
      created_at: "2026-01-01T00:00:00",
      updated_at: "2026-01-01T00:00:00",
    },
  ],
};

const RETAILER: Retailer = {
  id: 5,
  name: "Flipkart",
  slug: "flipkart",
  website: null,
  is_active: true,
  created_at: "2026-01-01T00:00:00",
  updated_at: "2026-01-01T00:00:00",
};

const LISTING: RetailerListingListItem = {
  id: 20,
  retailer_id: 5,
  product_variant_id: 10,
  seller_name: null,
  external_listing_id: null,
  product_url: "https://www.flipkart.com/x",
  listing_title: "Nothing Phone (3a), 128GB",
  availability: "in_stock",
  is_demo: false,
  created_at: "2026-01-01T00:00:00",
  updated_at: "2026-01-01T00:00:00",
  latest_price: 24999,
  latest_observed_at: "2026-01-01T00:00:00",
};

describe("DataExplorer", () => {
  beforeEach(() => {
    vi.mocked(api.listProducts).mockResolvedValue([PRODUCT]);
    vi.mocked(api.listRetailers).mockResolvedValue([RETAILER]);
    vi.mocked(api.getProductDetail).mockResolvedValue(PRODUCT_DETAIL);
    vi.mocked(api.listRetailerListings).mockResolvedValue([LISTING]);
    vi.mocked(api.listPriceObservations).mockResolvedValue([]);
    vi.mocked(api.listOffers).mockResolvedValue([]);
    vi.mocked(api.getDealAssessment).mockResolvedValue({
      retailer_listing_id: 20,
      assessed_at: "2026-01-01T00:00:00",
      listing_availability: "in_stock",
      current_price: 24999,
      mrp: null,
      mrp_discount_percentage: null,
      lowest_observed_price: null,
      highest_observed_price: null,
      average_observed_price: null,
      guaranteed_discount_total: 0,
      conditional_discount_total: 0,
      cashback_total: 0,
      effective_price_guaranteed: null,
      potential_effective_price: null,
      signals: {
        has_price_history: false,
        observation_count: 0,
        price_dropped_from_previous_observation: null,
        lowest_observed_in_history: null,
        within_wishlist_target: null,
        within_wishlist_max: null,
        has_guaranteed_discount: false,
        has_conditional_offers: false,
        has_cashback_offers: false,
        is_available: true,
      },
      reasons: [],
      caveats: [],
    });
  });

  it("lists products from the backend", async () => {
    render(<DataExplorer />);
    await waitFor(() => {
      expect(screen.getByText(/Nothing Phone 3a/)).toBeTruthy();
    });
  });

  it("shows an empty-state prompt, not fake data, when there are no products", async () => {
    vi.mocked(api.listProducts).mockResolvedValue([]);
    render(<DataExplorer />);
    await waitFor(() => {
      expect(screen.getByText(/No products tracked yet/i)).toBeTruthy();
    });
  });

  it("drills down: selecting a product reveals its variants", async () => {
    render(<DataExplorer />);
    await waitFor(() => expect(screen.getByText(/Nothing Phone 3a/)).toBeTruthy());

    fireEvent.click(screen.getByText(/Nothing Phone 3a/));

    await waitFor(() => {
      expect(screen.getByText(/8GB RAM/)).toBeTruthy();
    });
  });

  it("shows honest empty states for price history and offers, never fabricated data", async () => {
    render(<DataExplorer />);
    await waitFor(() => expect(screen.getByText(/Nothing Phone 3a/)).toBeTruthy());
    fireEvent.click(screen.getByText(/Nothing Phone 3a/));
    await waitFor(() => expect(screen.getByText(/8GB RAM/)).toBeTruthy());
    fireEvent.click(screen.getByText(/8GB RAM/));

    await waitFor(() => {
      expect(screen.getByText(/Flipkart/)).toBeTruthy();
    });
    fireEvent.click(screen.getByText(/Flipkart/));

    await waitFor(() => {
      expect(screen.getByText("No price history available yet.")).toBeTruthy();
      expect(screen.getByText("No offers available.")).toBeTruthy();
    });
  });

  it("badges demo data so it can never be mistaken for a real observed price", async () => {
    vi.mocked(api.listProducts).mockResolvedValue([{ ...PRODUCT, is_demo: true }]);
    render(<DataExplorer />);
    await waitFor(() => {
      expect(screen.getByText("Demo")).toBeTruthy();
    });
  });
});
