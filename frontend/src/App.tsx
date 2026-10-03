import { useEffect, useRef, useState } from "react";
import { Header, type DashboardView } from "./components/layout/Header";
import { SystemStatusPanel } from "./components/layout/SystemStatusPanel";
import { HuntInput } from "./components/hunt/HuntInput";
import { DealFeed } from "./components/deals/DealFeed";
import { WishlistPanel } from "./components/wishlist/WishlistPanel";
import { ActivityLog } from "./components/activity/ActivityLog";
import { DataExplorer } from "./components/explorer/DataExplorer";
import { useHealth } from "./hooks/useHealth";
import { useWishlists } from "./hooks/useWishlists";
import { useActivityLog } from "./hooks/useActivityLog";
import type { WishlistCreateInput } from "./types/wishlist";

function App() {
  const [activeView, setActiveView] = useState<DashboardView>("dashboard");
  const { status: backendStatus, health } = useHealth();
  const wishlists = useWishlists();
  const { entries, log } = useActivityLog();

  // Log each connect/disconnect transition once, not on every health poll.
  const wasConnected = useRef(false);
  useEffect(() => {
    if (backendStatus === "connected" && !wasConnected.current) {
      wasConnected.current = true;
      log("Backend connected");
    } else if (backendStatus === "offline" && wasConnected.current) {
      wasConnected.current = false;
      log("Backend connection lost");
    }
  }, [backendStatus, log]);

  const loggedDbOnce = useRef(false);
  useEffect(() => {
    if (health?.database === "connected" && !loggedDbOnce.current) {
      loggedDbOnce.current = true;
      log("Database initialized");
    }
  }, [health, log]);

  async function handleAddToWishlist(data: WishlistCreateInput) {
    const created = await wishlists.add(data);
    log(`Wishlist created: ${created.name}`);
    return created;
  }

  async function handleDelete(id: number) {
    const item = wishlists.items.find((entry) => entry.id === id);
    await wishlists.remove(id);
    log(`Wishlist removed: ${item?.name ?? `#${id}`}`);
  }

  return (
    <div className="min-h-screen bg-base">
      <Header activeView={activeView} onViewChange={setActiveView} />

      {activeView === "dashboard" ? (
        <>
          <HuntInput onSubmit={handleAddToWishlist} />

          <main className="mx-auto grid max-w-7xl grid-cols-1 gap-4 px-6 pb-10 lg:grid-cols-[1fr_22rem]">
            <DealFeed />
            <div className="flex flex-col gap-4">
              <SystemStatusPanel backendStatus={backendStatus} health={health} />
              <WishlistPanel
                items={wishlists.items}
                loading={wishlists.loading}
                error={wishlists.error}
                onDelete={handleDelete}
              />
              <ActivityLog entries={entries} />
            </div>
          </main>
        </>
      ) : (
        <DataExplorer />
      )}
    </div>
  );
}

export default App;
