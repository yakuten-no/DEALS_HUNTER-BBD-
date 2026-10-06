import { describe, expect, it } from "vitest";
import { act, renderHook } from "@testing-library/react";
import { useFetch } from "./useFetch";

/** A promise the test settles by hand, so the timing of every request is explicit. */
interface Deferred<T> {
  promise: Promise<T>;
  resolve: (value: T) => void;
  reject: (reason: unknown) => void;
}

function deferred<T>(): Deferred<T> {
  let resolve!: (value: T) => void;
  let reject!: (reason: unknown) => void;
  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

/** Mounts useFetch keyed on `id`: id 1 uses `first`, id 2 uses `second`. */
function renderTwoRequests<T>() {
  const first = deferred<T>();
  const second = deferred<T>();
  const requests = { 1: first, 2: second };
  const hook = renderHook(({ id }: { id: 1 | 2 }) => useFetch(() => requests[id].promise, [id]), {
    initialProps: { id: 1 as 1 | 2 },
  });
  return { first, second, ...hook };
}

describe("useFetch", () => {
  it("clears the previous data as soon as a request for new dependencies starts", async () => {
    const { result, rerender, first, second } = renderTwoRequests<string>();
    await act(async () => {
      first.resolve("old");
    });
    expect(result.current).toEqual({ data: "old", loading: false, error: null });

    // New dependencies: the second request is still pending, so nothing from
    // the first request may remain visible.
    rerender({ id: 2 });
    expect(result.current).toEqual({ data: null, loading: true, error: null });

    await act(async () => {
      second.resolve("new");
    });
    expect(result.current).toEqual({ data: "new", loading: false, error: null });
  });

  it("exposes the error and keeps no previous data when the replacement request fails", async () => {
    const { result, rerender, first, second } = renderTwoRequests<string>();
    await act(async () => {
      first.resolve("old");
    });
    expect(result.current.data).toBe("old");

    rerender({ id: 2 });
    await act(async () => {
      second.reject(new Error("boom"));
    });
    expect(result.current).toEqual({ data: null, loading: false, error: "boom" });
  });

  it("treats a successful null result as the new data, not as 'keep the previous data'", async () => {
    const { result, rerender, first, second } = renderTwoRequests<string | null>();
    await act(async () => {
      first.resolve("old");
    });
    expect(result.current.data).toBe("old");

    rerender({ id: 2 });
    await act(async () => {
      second.resolve(null);
    });
    expect(result.current).toEqual({ data: null, loading: false, error: null });
  });

  it("ignores an older response that arrives after a newer request has started", async () => {
    const { result, rerender, first, second } = renderTwoRequests<string>();

    // The dependencies change while the first request is still in flight.
    rerender({ id: 2 });
    await act(async () => {
      second.resolve("new");
    });
    expect(result.current).toEqual({ data: "new", loading: false, error: null });

    // The older request finally resolves; it must not overwrite the newer result.
    await act(async () => {
      first.resolve("old");
    });
    expect(result.current).toEqual({ data: "new", loading: false, error: null });
  });

  it("ignores an older failure that arrives after a newer request has started", async () => {
    const { result, rerender, first, second } = renderTwoRequests<string>();

    rerender({ id: 2 });
    await act(async () => {
      second.resolve("new");
    });
    await act(async () => {
      first.reject(new Error("late failure"));
    });
    expect(result.current).toEqual({ data: "new", loading: false, error: null });
  });

  it("clears data, loading and error when the fetch function becomes null", async () => {
    const first = deferred<string>();
    const { result, rerender } = renderHook(
      ({ id }: { id: 1 | null }) => useFetch(id === null ? null : () => first.promise, [id]),
      { initialProps: { id: 1 as 1 | null } },
    );
    await act(async () => {
      first.resolve("old");
    });
    expect(result.current.data).toBe("old");

    rerender({ id: null });
    expect(result.current).toEqual({ data: null, loading: false, error: null });
  });
});