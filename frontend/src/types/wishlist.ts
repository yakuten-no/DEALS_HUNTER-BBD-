/**
 * Mirrors backend/app/models/wishlist.py. V0.1 has no shared-schema code
 * generation, so keep these two definitions in sync by hand when either
 * one changes.
 */
export interface WishlistEntry {
  id: number;
  name: string;
  raw_query: string;
  budget_target: number | null;
  budget_max: number | null;
  minimum_storage_gb: number | null;
  preferred_ram_gb: number | null;
  camera_priority: boolean | null;
  gaming_priority: boolean | null;
  battery_priority: boolean | null;
  wireless_charging_preferred: boolean | null;
  preferred_brands: string[] | null;
  preferred_os: string | null;
  created_at: string;
  updated_at: string;
}

/** Matches backend WishlistCreate: raw_query is required, everything else optional. */
export interface WishlistCreateInput {
  raw_query: string;
  name?: string;
  budget_target?: number | null;
  budget_max?: number | null;
  minimum_storage_gb?: number | null;
  preferred_ram_gb?: number | null;
  camera_priority?: boolean | null;
  gaming_priority?: boolean | null;
  battery_priority?: boolean | null;
  wireless_charging_preferred?: boolean | null;
  preferred_brands?: string[] | null;
  preferred_os?: string | null;
}

/** Matches backend WishlistUpdate: every field optional, only sent fields change. */
export type WishlistUpdateInput = Partial<WishlistCreateInput>;
