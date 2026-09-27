import { describe, expect, it, vi } from "vitest";
import { renderHook, waitFor } from "@testing-library/react";
import { useHealth } from "./useHealth";
import * as api from "../lib/api";

vi.mock("../lib/api");

describe("useHealth", () => {
  it("starts in 'checking' and moves to 'connected' when the health check succeeds", async () => {
    vi.mocked(api.getHealth).mockResolvedValue({
      status: "ok",
      service: "bbd-hunter",
      version: "0.1.0",
      database: "connected",
    });

    const { result, unmount } = renderHook(() => useHealth());

    expect(result.current.status).toBe("checking");
    await waitFor(() => expect(result.current.status).toBe("connected"));
    expect(result.current.health?.database).toBe("connected");

    unmount();
  });

  it("moves to 'offline' when the health check fails, without a stale health object", async () => {
    vi.mocked(api.getHealth).mockRejectedValue(new Error("network error"));

    const { result, unmount } = renderHook(() => useHealth());

    await waitFor(() => expect(result.current.status).toBe("offline"));
    expect(result.current.health).toBeNull();

    unmount();
  });
});
