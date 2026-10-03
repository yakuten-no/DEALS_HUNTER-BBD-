import type { ProductListItem } from "../../types/product";
import { DemoBadge } from "./DemoBadge";

interface ProductListPanelProps {
  products: ProductListItem[];
  loading: boolean;
  error: string | null;
  selectedProductId: number | null;
  onSelect: (productId: number) => void;
}

export function ProductListPanel({ products, loading, error, selectedProductId, onSelect }: ProductListPanelProps) {
  return (
    <section className="rounded-lg border border-base-hairline bg-base-panel p-4">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm text-ink-muted">Products</h2>
        <span className="font-mono text-xs text-ink-muted">{products.length}</span>
      </div>

      {loading && products.length === 0 && <p className="text-sm text-ink-muted">Loading...</p>}
      {error && <p className="text-sm text-signal-negative">{error}</p>}
      {!loading && !error && products.length === 0 && (
        <p className="text-sm text-ink-muted">
          No products tracked yet. Run the demo seed script to see the explorer populated, or add one via the API.
        </p>
      )}

      <ul className="flex flex-col gap-1.5">
        {products.map((product) => {
          const isSelected = product.id === selectedProductId;
          return (
            <li key={product.id}>
              <button
                type="button"
                onClick={() => onSelect(product.id)}
                className={`flex w-full items-center justify-between gap-2 rounded-md border px-3 py-2 text-left transition-colors ${
                  isSelected
                    ? "border-signal-amber/60 bg-signal-amber/10"
                    : "border-base-hairline bg-base hover:border-signal-amber/30"
                }`}
              >
                <span className="min-w-0 flex-1">
                  <span className="block truncate text-sm text-ink">
                    {product.brand} {product.model_name}
                  </span>
                  <span className="block text-xs text-ink-muted">{product.category}</span>
                </span>
                <span className="flex flex-shrink-0 items-center gap-1.5">
                  {product.is_demo && <DemoBadge />}
                  <span className="font-mono text-xs text-ink-muted">
                    {product.variant_count} {product.variant_count === 1 ? "variant" : "variants"}
                  </span>
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
