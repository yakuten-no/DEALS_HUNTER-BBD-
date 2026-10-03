import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import App from "./App";
import * as api from "./lib/api";

// Auto-mocked: every export of ./lib/api becomes a vi.fn(). Individual
// tests configure the return values they need below.
vi.mock("./lib/api");

describe("App", () => {
  beforeEach(() => {
    vi.mocked(api.getHealth).mockResolvedValue({
      status: "ok",
      service: "bbd-hunter",
      version: "0.1.0",
      database: "connected",
    });
    vi.mocked(api.listWishlists).mockResolvedValue([]);
    // Only reached if a test switches to the Data Explorer tab -- harmless
    // to configure unconditionally for tests that never do.
    vi.mocked(api.listProducts).mockResolvedValue([]);
    vi.mocked(api.listRetailers).mockResolvedValue([]);
  });

  it("renders the BBD Hunter branding", () => {
    render(<App />);
    expect(screen.getByText(/BBD Hunter/i)).toBeTruthy();
  });

  it("shows the hunt input with its placeholder prompt", () => {
    render(<App />);
    expect(screen.getByPlaceholderText(/great camera/i)).toBeTruthy();
  });

  it("reflects a real backend connection once the health check succeeds", async () => {
    render(<App />);
    await waitFor(() => {
      // "Connected" appears for both Backend and Database once healthy.
      expect(screen.getAllByText("Connected").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows the backend as offline when the health check fails", async () => {
    vi.mocked(api.getHealth).mockRejectedValue(new Error("network error"));
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText("Offline")).toBeTruthy();
    });
  });

  it("shows an honest empty state for the wishlist and never fabricates deal data", async () => {
    render(<App />);
    await waitFor(() => {
      expect(screen.getByText(/Nothing tracked yet/i)).toBeTruthy();
    });
    // The deal feed must not claim to have found anything real yet.
    expect(screen.getByText(/No deals tracked yet/i)).toBeTruthy();
  });

  it("always shows AI and Collectors as inactive -- V0.1 has neither", () => {
    render(<App />);
    expect(screen.getByText("Not connected")).toBeTruthy();
    expect(screen.getByText("Not running")).toBeTruthy();
  });

  it("switches to the Data Explorer when its tab is clicked, and back again", () => {
    render(<App />);
    expect(screen.getByPlaceholderText(/great camera/i)).toBeTruthy(); // dashboard view by default

    fireEvent.click(screen.getByRole("button", { name: "Data Explorer" }));
    // Disambiguated from the still-visible tab button of the same name via role.
    expect(screen.getByRole("heading", { name: "Data Explorer" })).toBeTruthy();
    expect(screen.queryByPlaceholderText(/great camera/i)).toBeNull(); // dashboard content is gone, not just hidden

    fireEvent.click(screen.getByRole("button", { name: "Dashboard" }));
    expect(screen.getByPlaceholderText(/great camera/i)).toBeTruthy();
  });
});
