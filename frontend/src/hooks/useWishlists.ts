import { useCallback, useEffect, useState } from "react";
import { createWishlist, deleteWishlist, listWishlists, updateWishlist } from "../lib/api";
import type { WishlistCreateInput, WishlistEntry, WishlistUpdateInput } from "../types/wishlist";

/**
 * Loads the wishlist from the backend and exposes CRUD actions that keep
 * local state in sync with what was actually persisted (rather than
 * guessing the result client-side and hoping the server agrees).
 */
export function useWishlists() {
  const [items, setItems] = useState<WishlistEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setLoading(true);
      const data = await listWishlists();
      setItems(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load wishlist");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const add = useCallback(async (data: WishlistCreateInput) => {
    const created = await createWishlist(data);
    setItems((prev) => [created, ...prev]);
    return created;
  }, []);

  // Not wired to any UI control yet in V0.1 (no edit form) -- the backend
  // endpoint and this action both work and are tested, ready for a future
  // edit UI without changes here. See project-memory/CURRENT_STATE.md.
  const edit = useCallback(async (id: number, data: WishlistUpdateInput) => {
    const updated = await updateWishlist(id, data);
    setItems((prev) => prev.map((item) => (item.id === id ? updated : item)));
    return updated;
  }, []);

  const remove = useCallback(async (id: number) => {
    await deleteWishlist(id);
    setItems((prev) => prev.filter((item) => item.id !== id));
  }, []);

  return { items, loading, error, refresh, add, edit, remove };
}
