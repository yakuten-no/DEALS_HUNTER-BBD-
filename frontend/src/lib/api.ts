import type { WishlistCreateInput, WishlistEntry, WishlistUpdateInput } from "../types/wishlist";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  database: "connected" | "error" | string;
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
