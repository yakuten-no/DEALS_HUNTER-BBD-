import { useEffect, useState, type DependencyList } from "react";

interface FetchState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

/**
 * A small generic fetch-on-mount(-and-on-dependency-change) hook, used by
 * the Data Explorer's several read-only hooks (useProducts, useListings,
 * usePriceHistory, ...) so each of them doesn't repeat the same
 * loading/error/cancellation boilerplate as useWishlists/useHealth
 * already have their own versions of for V0.1's specific needs.
 *
 * Pass `fetchFn` as `null` when there's nothing to fetch yet (e.g. no
 * product selected) -- this clears the data instead of calling anything.
 *
 * `deps` is taken separately from `fetchFn` deliberately: `fetchFn` is
 * usually a fresh closure on every render, and re-running the effect
 * every render (rather than only when the *meaningful* inputs change)
 * would be wrong. This is a standard, deliberate trade-off for a small
 * generic fetch hook, not an oversight.
 */
export function useFetch<T>(fetchFn: (() => Promise<T>) | null, deps: DependencyList): FetchState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(fetchFn !== null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (fetchFn === null) {
      setData(null);
      setLoading(false);
      setError(null);
      return;
    }

    let cancelled = false;
    setLoading(true);
    setError(null);

    fetchFn()
      .then((result) => {
        if (!cancelled) setData(result);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps -- deps is the caller's explicit, meaningful dependency list; see docstring
  }, deps);

  return { data, loading, error };
}
