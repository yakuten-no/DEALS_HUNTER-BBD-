import { WishlistItem } from "./WishlistItem";
import type { WishlistEntry } from "../../types/wishlist";

interface WishlistPanelProps {
  items: WishlistEntry[];
  loading: boolean;
  error: string | null;
  onDelete: (id: number) => void;
}

export function WishlistPanel({ items, loading, error, onDelete }: WishlistPanelProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm text-ink-muted">Wishlist</h2>
        <span className="font-mono text-xs text-ink-muted">{items.length}</span>
      </div>

      {loading && items.length === 0 && <p className="text-sm text-ink-muted">Loading...</p>}
      {error && <p className="text-sm text-signal-negative">{error}</p>}
      {!loading && !error && items.length === 0 && (
        <p className="text-sm text-ink-muted">Nothing tracked yet. Describe a phone above to add your first entry.</p>
      )}

      <ul className="flex flex-col gap-2">
        {items.map((item) => (
          <WishlistItem key={item.id} item={item} onDelete={onDelete} />
        ))}
      </ul>
    </section>
  );
}
